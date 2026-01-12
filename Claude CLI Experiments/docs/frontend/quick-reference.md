# Frontend Agent - Quick Reference

## 🎯 Command

```
/frontend
```

## 8-Agent Team Structure

| Agent | Focus | Key Outputs |
|-------|-------|-------------|
| **1. Design System** | Tokens, patterns, themes | Design tokens, atomic components, Storybook |
| **2. Component Dev** | React/Vue/Angular components | Type-safe components, props APIs, hooks |
| **3. State Management** | App state, forms, server state | XState machines, Zustand stores, React Query |
| **4. Animation** | 60 FPS interactions | GSAP timelines, Framer Motion, micro-interactions |
| **5. Performance** | <200KB bundles, lazy loading | Code splitting, virtual scrolling, memoization |
| **6. Accessibility** | WCAG AA compliance | Keyboard nav, ARIA, screen reader optimization |
| **7. Responsive** | Mobile-first design | Breakpoints, fluid typography, container queries |
| **8. Testing/QA** | >80% coverage | Unit, component, E2E, visual regression tests |

## Performance Targets

✅ **Bundle Size:** <200KB initial load
✅ **FPS:** 60 FPS for all animations
✅ **LCP:** <2.5s (Largest Contentful Paint)
✅ **FID:** <100ms (First Input Delay)
✅ **CLS:** <0.1 (Cumulative Layout Shift)
✅ **TTI:** <3.5s (Time to Interactive)

## Accessibility Requirements

✅ **WCAG Level AA** (minimum target)
✅ **Keyboard Navigation:** All functionality accessible
✅ **Screen Readers:** Tested with NVDA/JAWS/VoiceOver
✅ **Color Contrast:** 4.5:1 minimum for normal text
✅ **Focus Indicators:** Visible on all interactive elements
✅ **ARIA:** Used where semantic HTML insufficient

## Technology Stack

### Frameworks
- React 19, Next.js 15
- Vue 3, Nuxt 3
- Angular 18
- Svelte 5

### Styling
- **Tailwind CSS** (recommended)
- CSS Modules
- Styled Components

### State Management
- **Zustand** (lightweight)
- **Redux Toolkit** (enterprise)
- **XState** (state machines)
- **TanStack Query** (server state)

### Animation
- **GSAP** (complex animations)
- **Framer Motion** (React-friendly)

### Testing
- **Vitest** (unit)
- **Playwright** (E2E)
- **Chromatic** (visual regression)
- **axe DevTools** (accessibility)

## 5-Phase Workflow

### Phase 1: Design Analysis
**Input:** Figma mockups, brand guidelines
**Output:** Design tokens, component specs

### Phase 2: Architecture
**Output:** Component hierarchy, state strategy

### Phase 3: Parallel Development
**Duration:** 4x faster than sequential
All 8 agents work simultaneously

### Phase 4: Testing
**Coverage:** Unit, component, visual, E2E, a11y, performance

### Phase 5: Optimization & Deploy
**Activities:** Bundle optimization, monitoring setup

## Common Patterns

### Component Pattern
```typescript
interface ButtonProps {
  variant: 'default' | 'destructive' | 'outline';
  size: 'sm' | 'md' | 'lg';
  loading?: boolean;
}

const Button = ({ variant, size, loading, children }: ButtonProps) => (
  <button className={cn(buttonVariants({ variant, size }))}>
    {loading && <Spinner />}
    {children}
  </button>
);
```

### State Machine Pattern
```typescript
const machine = createMachine({
  initial: 'idle',
  states: {
    idle: { on: { START: 'loading' } },
    loading: { on: { SUCCESS: 'success', ERROR: 'error' } },
    success: { on: { RESET: 'idle' } },
    error: { on: { RETRY: 'loading' } },
  },
});
```

### Animation Pattern
```typescript
gsap.timeline()
  .from('.hero', { opacity: 0, y: 50 })
  .from('.cta', { opacity: 0, scale: 0.8 }, '-=0.3');
```

### Performance Pattern
```typescript
const Dashboard = lazy(() => import('./Dashboard'));

<Suspense fallback={<Skeleton />}>
  <Dashboard />
</Suspense>
```

## Testing Pyramid

```
      /\
     /E2E\        5% - Critical user flows
    /------\
   /Visual \      10% - UI consistency
  /----------\
 /Integration\    15% - Component interactions
/--------------\
/    Unit      \  70% - Component logic
/----------------\
```

## When to Use Which Specialist

| Specialist | Use For |
|------------|---------|
| **Design System** | New project, component library, design tokens |
| **Component Dev** | UI implementation, forms, layouts |
| **State Management** | Complex state, multi-step forms, auth flows |
| **Animation** | Page transitions, micro-interactions, scroll effects |
| **Performance** | Slow loads, large apps, mobile optimization |
| **Accessibility** | Public sites, government, healthcare, finance |
| **Responsive** | Multi-device support, mobile apps |
| **Testing/QA** | Production apps, CI/CD, quality assurance |

## Best Practices Checklist

### Component Development
- [ ] Single Responsibility Principle
- [ ] TypeScript for type safety
- [ ] Storybook documentation
- [ ] Unit tests >80% coverage
- [ ] Accessible by default

### State Management
- [ ] Appropriate solution selected
- [ ] Minimize prop drilling
- [ ] Optimize re-renders
- [ ] Cache server state
- [ ] Persist when needed

### Performance
- [ ] Code split by route
- [ ] Lazy load components
- [ ] Optimize images (WebP)
- [ ] Memoize expensive computations
- [ ] Monitor Core Web Vitals

### Accessibility
- [ ] Semantic HTML
- [ ] Keyboard navigation
- [ ] ARIA where needed
- [ ] Color contrast 4.5:1+
- [ ] Screen reader tested

### Testing
- [ ] Unit tests for logic
- [ ] Component tests for UI
- [ ] E2E for critical flows
- [ ] Visual regression
- [ ] Performance budgets

## Success Metrics

**Development Velocity:**
- **4x faster** feature implementation
- **90.2% better** than single-agent
- **40-60% cheaper** through specialization

**Quality Metrics:**
- **>80% test coverage**
- **WCAG AA compliance**
- **60 FPS animations**
- **<200KB bundles**
- **Core Web Vitals green**

## Troubleshooting

### Issue: Slow Animations
**Solution:** Use transform/opacity only, enable GPU acceleration

### Issue: Large Bundle Size
**Solution:** Code splitting, lazy load routes, analyze with Bundle Analyzer

### Issue: Accessibility Violations
**Solution:** Run axe DevTools, test with screen readers, fix ARIA issues

### Issue: Failed E2E Tests
**Solution:** Add explicit waits, use stable selectors, check flaky tests

### Issue: Poor Mobile Performance
**Solution:** Optimize images, reduce JS, implement virtual scrolling

## Resources

**Documentation:**
- React: https://react.dev
- Next.js: https://nextjs.org/docs
- Tailwind: https://tailwindcss.com/docs
- WCAG: https://www.w3.org/WAI/WCAG21/quickref/

**Tools:**
- Figma - Design collaboration
- Storybook - Component documentation
- Chromatic - Visual regression
- Lighthouse - Performance audits
- axe DevTools - Accessibility testing

---

**Version:** 2.0
**Last Updated:** 2025-10-21
**Quick Access:** Use `/frontend` to activate the elite 8-agent team
