# ADR-005: Frontend State Management Strategy

Date: 2025-10-24

## Status
**NEEDS REVIEW** - Performance Concerns at Current Scale

## Context

The ASR Ops Dashboard React frontend has grown significantly:
- **96+ React components** (pages, cards, forms, modals)
- **Multiple contexts:** AuthContext, AppContext
- **Complex state requirements:**
  - Authentication state (user, token, permissions)
  - Application state (projects, timecards, reports)
  - UI state (modals, filters, selected items)
  - Form state (multi-step forms, validation)
  - Cache state (API responses)

### Current Implementation: React Context API

**AuthContext:**
```javascript
- currentUser (user object)
- token (JWT access token)
- login() / logout()
- isAuthenticated
```

**AppContext:**
```javascript
- Global app state
- Shared data across components
- Loading states
- Error handling
```

### Problems Identified

**Performance Issues:**
- Context changes trigger re-renders of ALL consumers
- 96+ components may subscribe to contexts unnecessarily
- No built-in memoization or selector optimization
- Large context values cause full component tree re-renders

**Developer Experience:**
- Context nesting becomes deep (Provider hell)
- Difficult to debug state changes
- No dev tools for state inspection
- Unclear data flow with multiple contexts

**Scalability:**
- Adding new state requires new contexts or expanding existing ones
- Context splitting is manual and error-prone
- No standard patterns for async actions
- Difficult to test components with context dependencies

## Decision Options

## Option A: Zustand (RECOMMENDED)

### Overview
Lightweight state management with hooks-based API and built-in selectors.

### Implementation

```javascript
// stores/authStore.js
import create from 'zustand';
import { persist } from 'zustand/middleware';

export const useAuthStore = create(
  persist(
    (set, get) => ({
      currentUser: null,
      token: null,

      login: async (credentials) => {
        const { token, user } = await api.login(credentials);
        set({ token, currentUser: user });
      },

      logout: () => {
        set({ token: null, currentUser: null });
      },

      isAuthenticated: () => !!get().token,
    }),
    {
      name: 'auth-storage',
      getStorage: () => sessionStorage,
    }
  )
);

// Usage in components
function Dashboard() {
  const currentUser = useAuthStore(state => state.currentUser); // Selective subscription
  const logout = useAuthStore(state => state.logout);

  // Only re-renders when currentUser changes
}
```

**State Structure:**
```javascript
// stores/projectsStore.js
export const useProjectsStore = create((set) => ({
  projects: [],
  selectedProject: null,
  filters: { status: 'ACTIVE' },
  loading: false,

  fetchProjects: async (filters) => {
    set({ loading: true });
    const projects = await api.getProjects(filters);
    set({ projects, loading: false });
  },

  selectProject: (project) => set({ selectedProject: project }),

  updateFilters: (filters) => set({ filters }),
}));
```

### Pros
- **Lightweight:** ~1KB gzipped
- **Simple API:** Familiar hooks-based syntax
- **Selective subscriptions:** Components only re-render when selected state changes
- **No Provider wrapping:** Direct store access
- **Built-in persistence:** LocalStorage/SessionStorage middleware
- **DevTools:** Zustand DevTools extension available
- **TypeScript support:** Excellent type inference
- **Async actions:** Built-in, no middleware needed
- **Easy testing:** Mock stores directly

### Cons
- Smaller ecosystem than Redux
- Less opinionated (need to establish patterns)
- No time-travel debugging (unlike Redux DevTools)

### Migration Effort
- **Low to Medium:** Incremental migration possible
- Migrate AuthContext first (highest impact)
- Keep existing Context API during transition
- Estimate: 2-3 weeks for full migration

---

## Option B: Redux Toolkit

### Overview
Official, opinionated Redux toolset with modern patterns.

### Implementation

```javascript
// features/auth/authSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

export const loginAsync = createAsyncThunk(
  'auth/login',
  async (credentials) => {
    const response = await api.login(credentials);
    return response.data;
  }
);

const authSlice = createSlice({
  name: 'auth',
  initialState: { user: null, token: null, status: 'idle' },
  reducers: {
    logout: (state) => {
      state.user = null;
      state.token = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(loginAsync.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(loginAsync.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.user = action.payload.user;
        state.token = action.payload.token;
      });
  },
});

// Usage
import { useSelector, useDispatch } from 'react-redux';

function Dashboard() {
  const user = useSelector(state => state.auth.user);
  const dispatch = useDispatch();

  const handleLogout = () => dispatch(authSlice.actions.logout());
}
```

### Pros
- **Industry standard:** Large community and ecosystem
- **Excellent DevTools:** Time-travel debugging, action history
- **Middleware ecosystem:** Redux Saga, Redux Thunk
- **Strong TypeScript support**
- **Well-documented:** Extensive official docs and tutorials
- **Predictable:** Strict patterns reduce bugs

### Cons
- **Larger bundle:** ~8KB + react-redux ~6KB
- **More boilerplate:** Actions, reducers, slices
- **Steeper learning curve:** More concepts to learn
- **Provider wrapping required**
- **Overkill for simple state:** Better for complex applications

### Migration Effort
- **Medium to High:** More setup required
- Need to configure store, middleware
- More files and structure to create
- Estimate: 3-4 weeks for full migration

---

## Option C: Keep Context API with Optimizations

### Overview
Optimize current Context API usage with performance best practices.

### Implementation

```javascript
// Optimized AuthContext
const AuthContext = createContext();

function AuthProvider({ children }) {
  const [auth, setAuth] = useState({ user: null, token: null });

  // Memoize auth value to prevent unnecessary re-renders
  const authValue = useMemo(() => ({
    currentUser: auth.user,
    token: auth.token,
    login: async (credentials) => { /* ... */ },
    logout: () => { /* ... */ },
  }), [auth]);

  return (
    <AuthContext.Provider value={authValue}>
      {children}
    </AuthContext.Provider>
  );
}

// Split contexts by update frequency
const AuthStateContext = createContext(); // Rarely changes
const AuthActionsContext = createContext(); // Never changes

// Use selectors
function useAuthState(selector) {
  const state = useContext(AuthStateContext);
  return selector(state);
}
```

### Pros
- **No new dependencies**
- **Familiar to team**
- **Minimal migration**
- **React-native solution**

### Cons
- **Manual optimization required**
- **Still performance issues at scale**
- **No dev tools**
- **Complex to manage many contexts**
- **Doesn't solve root problems**

### Migration Effort
- **Low:** Optimize existing code
- Add memoization and context splitting
- Estimate: 1 week

---

## Recommended Decision: Option A (Zustand)

### Rationale

**Performance:**
- Selective subscriptions prevent unnecessary re-renders
- Proven to scale to 100+ components
- Minimal bundle size impact (1KB)

**Developer Experience:**
- Simple, intuitive API
- Easy debugging with DevTools
- Clear data flow
- Great TypeScript support

**Migration Path:**
- Incremental migration (can coexist with Context)
- Start with highest-impact areas (AuthContext)
- Low risk, high reward

**Team Fit:**
- Small learning curve
- Hooks-based (familiar pattern)
- Less boilerplate than Redux

**Future-Proof:**
- Scales well beyond current needs
- Active community
- Easy to extract stores if moving to micro-frontends

### Implementation Plan

**Phase 1: Setup (Week 1)**
```bash
npm install zustand
```

```javascript
// stores/index.js - Central export
export { useAuthStore } from './authStore';
export { useProjectsStore } from './projectsStore';
export { useTimecardStore } from './timecardStore';
```

**Phase 2: Migrate AuthContext (Week 1-2)**
- Create `stores/authStore.js`
- Replace `AuthContext.Provider` with Zustand store
- Update all `useContext(AuthContext)` to `useAuthStore`
- Remove old AuthContext file
- Test authentication flows

**Phase 3: Migrate AppContext (Week 2-3)**
- Split AppContext into domain stores:
  - `projectsStore.js` (projects, filters)
  - `uiStore.js` (modals, notifications, theme)
  - `cacheStore.js` (API response caching)
- Migrate components incrementally
- Remove old AppContext

**Phase 4: Add Persistence (Week 3)**
```javascript
// Persist auth and UI preferences
import { persist } from 'zustand/middleware';

export const useAuthStore = create(
  persist(
    (set, get) => ({ /* ... */ }),
    { name: 'auth-storage' }
  )
);
```

**Phase 5: DevTools Integration (Week 3)**
```javascript
import { devtools } from 'zustand/middleware';

export const useProjectsStore = create(
  devtools(
    (set) => ({ /* ... */ }),
    { name: 'Projects Store' }
  )
);
```

**Phase 6: Testing & Optimization (Week 4)**
- Performance testing with React DevTools Profiler
- Optimize selector usage
- Add store-level tests
- Documentation for team

### Code Examples

**Before (Context API):**
```javascript
// Components re-render on ANY auth context change
function ProjectCard() {
  const { currentUser, token, login, logout } = useContext(AuthContext);
  // Only needs currentUser, but re-renders on any auth change

  return <div>Project Manager: {currentUser?.name}</div>;
}
```

**After (Zustand):**
```javascript
// Component only re-renders when currentUser changes
function ProjectCard() {
  const currentUser = useAuthStore(state => state.currentUser);

  return <div>Project Manager: {currentUser?.name}</div>;
}

// Actions don't cause re-renders when unused
function LogoutButton() {
  const logout = useAuthStore(state => state.logout);

  return <button onClick={logout}>Logout</button>;
}
```

**Store Organization:**
```
src/
└── stores/
    ├── index.js           # Central export
    ├── authStore.js       # Authentication
    ├── projectsStore.js   # Projects, filters
    ├── timecardsStore.js  # Timecards, time entries
    ├── uiStore.js         # Modals, notifications, theme
    ├── cacheStore.js      # API response caching
    └── __tests__/         # Store tests
```

## Consequences

### Positive Consequences

**Performance Improvement:**
- **Expected:** 60-80% reduction in unnecessary re-renders
- Faster UI interactions
- Smoother scrolling and animations
- Better user experience on lower-end devices

**Developer Productivity:**
- Faster development with simpler API
- Easier debugging with DevTools
- Clear data flow
- Better code organization

**Maintainability:**
- Centralized state logic
- Easier to test
- Clear patterns for new features
- Reduced coupling between components

**Scalability:**
- Can scale to 200+ components
- Easy to add new stores
- No performance degradation with growth

### Negative Consequences

**Migration Effort:**
- 4 weeks of development time
- Temporary code duplication during migration
- Risk of regression bugs
- Team training required

**New Dependency:**
- +1KB bundle size (negligible)
- New library to maintain
- Dependency risk (small library)

**Learning Curve:**
- Team needs to learn Zustand patterns
- Documentation required
- Code review adjustments

### Risks and Mitigation

**Risk: Migration introduces bugs**
- **Mitigation:** Incremental migration (coexist with Context)
- **Mitigation:** Comprehensive testing for each migrated area
- **Mitigation:** Feature flags for gradual rollout

**Risk: Performance issues not resolved**
- **Mitigation:** Benchmark before/after with React Profiler
- **Mitigation:** Can roll back to Context if needed
- **Mitigation:** Monitor performance metrics in production

**Risk: Team resistance to change**
- **Mitigation:** Demo performance improvements
- **Mitigation:** Provide training and documentation
- **Mitigation:** Start with small, high-impact migration (Auth)

## Success Metrics

**Performance:**
- Reduce re-renders by 60-80% (measure with React Profiler)
- Improve page load time by 20-30%
- Reduce time-to-interactive by 15-25%

**Developer Experience:**
- Faster feature development (measure velocity)
- Reduced bugs related to state management
- Positive team feedback

**Code Quality:**
- Improved test coverage for state logic
- Reduced component complexity
- Better separation of concerns

## Related Decisions

- ADR-002: Monolithic Architecture (establishes React as frontend)
- ADR-004: RESTful API Design (affects how stores fetch data)
- Future ADR: Server State Management (React Query/SWR)

## References

- [Zustand Documentation](https://github.com/pmndrs/zustand)
- [React State Management in 2024](https://react.dev/learn/managing-state)
- [When to Use Context vs Zustand](https://blog.logrocket.com/zustand-vs-context-api/)

---

**Status:** AWAITING APPROVAL
**Owner:** Frontend Team
**Implementation Timeline:** 4 weeks
**Risk Level:** MEDIUM (migration complexity, but reversible)
**Next Review:** 2025-11-24 (after Phase 2 completion)
