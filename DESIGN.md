---
name: Precision Procurement
colors:
  surface: '#f6f9ff'
  surface-dim: '#d5dae1'
  surface-bright: '#f6f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4fb'
  surface-container: '#e9eef5'
  surface-container-high: '#e4e9f0'
  surface-container-highest: '#dee3ea'
  on-surface: '#171c21'
  on-surface-variant: '#45474c'
  inverse-surface: '#2b3136'
  inverse-on-surface: '#ecf1f8'
  outline: '#75777d'
  outline-variant: '#c5c6cc'
  surface-tint: '#565f70'
  primary: '#040d1b'
  on-primary: '#ffffff'
  primary-container: '#1a2332'
  on-primary-container: '#818a9d'
  inverse-primary: '#bec7db'
  secondary: '#0058be'
  on-secondary: '#ffffff'
  secondary-container: '#2170e4'
  on-secondary-container: '#fefcff'
  tertiary: '#150a00'
  on-tertiary: '#ffffff'
  tertiary-container: '#2e200b'
  on-tertiary-container: '#9c866a'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dae3f7'
  primary-fixed-dim: '#bec7db'
  on-primary-fixed: '#131c2a'
  on-primary-fixed-variant: '#3e4758'
  secondary-fixed: '#d8e2ff'
  secondary-fixed-dim: '#adc6ff'
  on-secondary-fixed: '#001a42'
  on-secondary-fixed-variant: '#004395'
  tertiary-fixed: '#f9debe'
  tertiary-fixed-dim: '#dcc3a3'
  on-tertiary-fixed: '#261905'
  on-tertiary-fixed-variant: '#55442c'
  background: '#f6f9ff'
  on-background: '#171c21'
  surface-variant: '#dee3ea'
  status-success: '#10B981'
  status-warning: '#F59E0B'
  status-error: '#EF4444'
  status-pending: '#6366F1'
  text-main: '#0F1419'
  text-muted: '#8B9CB3'
  surface-sidebar: '#1A2332'
typography:
  headline-lg:
    fontFamily: Manrope
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Manrope
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
  headline-md:
    fontFamily: Manrope
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-sm:
    fontFamily: Manrope
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  label-sm:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 14px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  container-padding: 24px
  gutter: 20px
---

## Brand & Style
The design system is built for a high-performance Enterprise SaaS environment. It targets procurement officers and financial controllers who require a focused, efficient, and trustworthy interface to manage complex data. 

The aesthetic is **Corporate / Modern**, characterized by a sophisticated "Deep Mode" sidebar and a "Light Mode" workspace. It emphasizes clarity through generous whitespace, a structured hierarchy, and a refined professional palette. The emotional response should be one of control, reliability, and precision. Every element is designed to minimize cognitive load while maximizing the visibility of critical tracking statuses.

## Colors
The color strategy utilizes a "Professional Depth" approach. The primary color is a deep, authoritative navy used for structural elements like sidebars and primary navigation to ground the interface. The secondary color is a vibrant digital blue, reserved for primary actions and focused state indicators.

Functional colors are critical for this design system:
- **Success:** Emerald green for "Completed" or "Paid" orders.
- **Warning:** Amber for "Delayed" or "Approval Needed."
- **Error:** Crimson for "Cancelled" or "Rejected" orders.
- **Pending:** Indigo for "In Progress" or "Draft" states.

Backgrounds use a soft off-white/gray to reduce eye strain during long working sessions, while the main text uses a near-black for maximum accessibility.

## Typography
The typography system pairs **Manrope** for headings and **Inter** for UI and body text. Manrope provides a modern, geometric clarity that feels high-end, while Inter is used for its exceptional legibility in data-heavy environments like tables and forms.

Headlines use a tighter letter-spacing and heavier weights to establish a strong visual anchor. Body text is optimized for readability with standard line heights. Labels are frequently used for table headers and status chips, employing uppercase styling and increased tracking to differentiate them from interactive text.

## Layout & Spacing
This design system utilizes a **Fixed-Fluid Hybrid Grid**. The main navigation sidebar is fixed at 280px, while the content area expands fluidly to fill the remaining screen real estate. 

A strict 4px baseline grid ensures vertical rhythm. Page layouts follow a 12-column grid system for desktop with 20px gutters. 
- **Mobile:** Single column with 16px side margins.
- **Tablet:** 8-column grid with 24px side margins.
- **Desktop:** 12-column grid with 32px side margins or a max-width container of 1440px for data density control.

Spacing between functional groups (like form sections) should default to `lg` (24px), while internal element spacing (like label to input) should use `sm` (8px).

## Elevation & Depth
Depth is conveyed through a combination of **Tonal Layering** and **Ambient Shadows**. 

The background layer is the lowest (`#E8EDF4`). Cards and primary containers sit on the middle layer (`#FFFFFF`) with a very subtle, diffused shadow (0px 2px 4px rgba(0,0,0,0.05)). 

Interactive elements like dropdowns, modals, and hovered cards use a higher elevation shadow (0px 10px 20px rgba(0,0,0,0.1)) to suggest they are closer to the user. We avoid heavy borders in favor of soft shadows and slight 1px strokes in a lighter neutral shade to define boundaries.

## Shapes
The shape language is consistently "Rounded" to soften the industrial nature of a tracking system. 
- **Standard UI elements** (Inputs, Buttons, Cards): 8px (0.5rem) corner radius.
- **Large containers** (Modals, Feature sections): 16px (1rem) corner radius.
- **Status Tags/Chips**: Fully rounded (pill-shaped) to distinguish them from clickable buttons.

Consistency in roundedness is vital to maintaining the sleek, professional aesthetic.

## Components
- **Buttons:** Primary buttons use the secondary blue color with white text. Secondary buttons use a light gray background with the primary navy text. Use an 8px radius.
- **Status Chips:** Small, pill-shaped indicators. Use low-opacity background tints of the status colors (e.g., 10% green) with high-saturation text for maximum readability without visual clutter.
- **Input Fields:** 1px stroke in a neutral-mid tone. On focus, the stroke should change to the secondary blue with a soft 2px outer glow.
- **Data Tables:** Clean, no vertical borders. Use thin horizontal separators. Headers should be `label-md` with a subtle gray background. Hover states on rows are mandatory for tracking accuracy.
- **Cards:** White background, 8px radius, and "Level 1" ambient shadow. Used to group PO details and summary metrics (Sankey-style or KPI cards).
- **Progress Trackers:** Vertical or horizontal steppers using the status color palette to indicate the current phase of a Purchase Order (Draft -> Approval -> Sent -> Received).