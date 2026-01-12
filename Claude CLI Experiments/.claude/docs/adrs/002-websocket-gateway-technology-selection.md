# ADR-002: WebSocket Gateway Technology Selection

**Date:** 2024-10-29
**Status:** Accepted
**Deciders:** Backend Team, Architecture Agent
**Technical Story:** Real-time Collaboration Platform - WebSocket Infrastructure

---

## Context

The event-driven architecture requires a WebSocket gateway to handle client connections and real-time communication. This gateway will:

- Manage 1000+ concurrent WebSocket connections
- Authenticate and authorize clients
- Subscribe to relevant events from message broker
- Push events to connected clients
- Handle connection lifecycle (connect, disconnect, reconnect)
- Support room-based messaging for collaboration spaces

**Requirements:**
- High concurrency (1000+ connections per instance)
- Low latency (<50ms event delivery)
- Automatic reconnection handling
- Broadcasting to rooms/channels
- Horizontal scaling capability
- Good monitoring and debugging tools

**Team Context:**
- Strong Node.js expertise
- Some experience with Python async frameworks
- Limited Go experience

---

## Decision

**We will use Node.js with Socket.io for the WebSocket gateway.**

**Technology Stack:**
- **Runtime:** Node.js 20.x LTS
- **Framework:** Socket.io 4.x
- **Redis Adapter:** For multi-instance scaling
- **Authentication:** JWT tokens validated at connection time
- **Deployment:** Kubernetes with HPA (Horizontal Pod Autoscaling)

**Architecture:**
```
Clients (Browser/Mobile)
    ↓ WebSocket
Socket.io Gateway Instances (Node.js)
    ↓ Redis Pub/Sub (Socket.io Adapter)
Message Broker (Redis Streams)
    ↓
Domain Services
```

---

## Consequences

### Positive Consequences

- **Performance:** Node.js event loop excellent for I/O-bound WebSocket operations
  - Can handle 10K+ connections per instance with 1GB RAM
  - Non-blocking I/O perfect for real-time messaging

- **Developer Productivity:** Team already experienced with Node.js
  - Faster development velocity
  - Easier debugging and maintenance
  - Rich ecosystem of libraries

- **Socket.io Features:** Built-in functionality for common use cases
  - Automatic reconnection with exponential backoff
  - Room/namespace support for collaboration spaces
  - Fallback to polling if WebSocket unavailable
  - Binary data support for file transfers

- **Scaling:** Socket.io Redis Adapter enables horizontal scaling
  - Add instances without code changes
  - Events broadcast across all instances automatically
  - Session affinity not required

- **Ecosystem:** Excellent tooling and community support
  - @socket.io/admin-ui for monitoring
  - Extensive middleware options
  - Good integration with monitoring tools

### Negative Consequences / Trade-offs

- **Memory Usage:** Node.js uses more memory than Go/Rust alternatives
  - **Mitigation:** Allocate 2GB RAM per instance
  - **Mitigation:** Kubernetes resource limits prevent memory leaks from crashing cluster
  - **Cost:** Slightly higher infrastructure costs (~20% more than Go equivalent)

- **Single-Threaded:** Can't utilize multiple CPU cores per process
  - **Mitigation:** Run multiple instances with load balancer
  - **Mitigation:** Kubernetes HPA scales horizontally based on CPU/connection count
  - **Impact:** Not a real issue with horizontal scaling strategy

- **Type Safety:** JavaScript's weak typing can cause runtime errors
  - **Mitigation:** Use TypeScript with strict mode enabled
  - **Mitigation:** Comprehensive unit tests for event handlers
  - **Mitigation:** Event schema validation with Zod

### Neutral Consequences

- **Language Consistency:** Backend primarily Node.js, some Python services
  - Mixed stack but acceptable given team expertise
  - Consider standardizing on Node.js for new services

---

## Alternatives Considered

### Alternative 1: Go with Gorilla WebSocket

**Description:** Go-based WebSocket server using Gorilla WebSocket library

**Pros:**
- Extremely efficient (lower memory, higher throughput)
- Built-in concurrency with goroutines
- Compiled binary (faster startup, smaller image)
- Lower infrastructure costs

**Cons:**
- Team has limited Go experience (learning curve)
- Fewer built-in features than Socket.io (must build ourselves)
- Smaller ecosystem for WebSocket-specific tooling
- Slower development velocity initially

**Why rejected:** Team productivity is more important than raw performance at MVP stage. Node.js meets performance requirements (1000+ connections validated). Can consider Go for future optimization if needed.

---

### Alternative 2: Python with FastAPI + WebSockets

**Description:** Python backend using FastAPI's WebSocket support

**Pros:**
- Team has Python experience
- FastAPI has excellent WebSocket support
- Good async/await model (similar to Node.js)
- Type hints with Pydantic

**Cons:**
- Python's async ecosystem less mature than Node.js for WebSockets
- Higher latency than Node.js for high-concurrency scenarios
- Fewer WebSocket-specific libraries and tools
- Socket.io-like features must be built manually

**Why rejected:** Node.js has better WebSocket performance and ecosystem. Python better suited for CPU-intensive services (data processing, ML). Use Python for domain services where it makes sense.

---

### Alternative 3: uWebSockets.js

**Description:** Ultra-fast WebSocket library for Node.js (C++ bindings)

**Pros:**
- Extremely fast (faster than Socket.io)
- Lower memory footprint
- Still Node.js ecosystem
- Great benchmarks

**Cons:**
- Less mature than Socket.io
- Fewer features out of the box
- Smaller community
- Must implement many features manually (rooms, reconnection, etc.)
- More C++ expertise needed for troubleshooting

**Why rejected:** Premature optimization. Socket.io meets performance requirements and provides many built-in features. If performance becomes bottleneck, can migrate later. Development speed more important at MVP stage.

---

## Research & References

1. [Socket.io Documentation](https://socket.io/docs/v4/) - Official docs
2. [Socket.io Scaling Guide](https://socket.io/docs/v4/using-multiple-nodes/) - Multi-instance scaling
3. [Node.js WebSocket Performance](https://medium.com/@alexergul/nodejs-websocket-performance-c68de49d93ce) - Benchmark comparison
4. [WebSocket Connection Limits](https://blog.jayway.com/2015/04/13/600k-concurrent-websocket-connections-on-aws-using-node-js/) - Scalability case study

### Research Query

```bash
/research Node.js Socket.io vs Go WebSocket performance comparison for real-time applications
```

**Key findings:**
- Node.js handles 10K connections/instance easily (with proper tuning)
- Go is faster but difference not significant at our scale (<1000 connections initially)
- Socket.io developer productivity advantage worth the slight performance trade-off
- Many successful real-time platforms use Socket.io (production-proven)

---

## Implementation Notes

### Prerequisites

1. **Infrastructure:**
   - Kubernetes cluster with Ingress controller
   - Redis cluster for Socket.io adapter
   - SSL/TLS certificates for WSS connections

2. **Development:**
   - TypeScript project setup with strict mode
   - Event schema definitions (shared with backend services)
   - JWT validation middleware
   - Connection rate limiting

### Implementation Steps

**Phase 1: Basic Gateway (Week 1)**
1. Initialize Node.js + TypeScript project
2. Setup Socket.io server with authentication
3. Implement JWT validation middleware
4. Add basic room management
5. Create health check endpoints

**Phase 2: Message Broker Integration (Week 2)**
6. Connect to Redis Streams message broker
7. Subscribe to relevant event topics
8. Implement event routing to Socket.io rooms
9. Add event acknowledgment system

**Phase 3: Scaling (Week 3)**
10. Configure Socket.io Redis Adapter
11. Test multi-instance deployment
12. Setup Kubernetes HPA
13. Load testing with 1000+ concurrent connections

**Phase 4: Monitoring (Week 4)**
14. Integrate Socket.io Admin UI
15. Add Prometheus metrics
16. Setup distributed tracing
17. Create operational dashboards

### Configuration

**Socket.io Server Options:**
```typescript
const io = new Server(httpServer, {
  cors: { origin: process.env.ALLOWED_ORIGINS },
  pingTimeout: 60000,
  pingInterval: 25000,
  upgradeTimeout: 10000,
  maxHttpBufferSize: 1e6, // 1MB
  transports: ['websocket', 'polling'],
  allowEIO3: false // Security: disable legacy protocol
});
```

**Redis Adapter:**
```typescript
import { createAdapter } from "@socket.io/redis-adapter";
import { createClient } from "redis";

const pubClient = createClient({ url: process.env.REDIS_URL });
const subClient = pubClient.duplicate();

io.adapter(createAdapter(pubClient, subClient));
```

### Timeline

- **Start Date:** 2024-11-01
- **Target Completion:** 2024-11-29 (4 weeks)
- **Production Ready:** 2024-12-06

### Success Criteria

- [ ] Handle 1000+ concurrent connections per instance
- [ ] <50ms event delivery latency (p95)
- [ ] Automatic reconnection working
- [ ] Zero-downtime deployments
- [ ] Room broadcasting functional
- [ ] Authentication and authorization working
- [ ] Monitoring dashboards operational
- [ ] Load tests passing (10K connections across cluster)

---

## Review & Update History

| Date | Author | Change | Reason |
|------|--------|--------|--------|
| 2024-10-29 | Backend Team | Created ADR | Technology selection for WebSocket gateway |
| 2024-10-29 | Backend Team | Status → Accepted | Team consensus after research |

---

## Related ADRs

- [ADR-001: Event-Driven Architecture](./001-event-driven-architecture-for-realtime-collab.md) - Overall architecture
- [ADR-003: Authentication Strategy](./003-authentication-strategy.md) - JWT implementation details
- [ADR-005: Horizontal Scaling Strategy](./005-horizontal-scaling-strategy.md) - Kubernetes HPA configuration

---

## Notes

**Performance Tuning:**

1. **Node.js Configuration:**
   ```bash
   NODE_ENV=production
   NODE_OPTIONS="--max-old-space-size=2048"
   UV_THREADPOOL_SIZE=128
   ```

2. **OS Tuning (Linux):**
   ```bash
   # Increase file descriptor limit
   ulimit -n 65536

   # TCP tuning
   net.ipv4.tcp_max_syn_backlog = 4096
   net.core.somaxconn = 4096
   ```

3. **Kubernetes Resources:**
   ```yaml
   resources:
     requests:
       cpu: 500m
       memory: 1Gi
     limits:
       cpu: 2000m
       memory: 2Gi
   ```

**Monitoring Metrics:**
- Active connections count
- Events/second throughput
- Latency percentiles (p50, p95, p99)
- Memory usage per instance
- Connection errors and disconnects

---

**Approved by:** Backend Team Lead, Architecture Team
**Implementation assigned to:** Backend Team
**Review Date:** 2024-12-15
