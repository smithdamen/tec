# TEC – GDD

## High Concept
Post-collapse survival sandbox: learn-by-doing, deep crafting, PVP with safe zones, seed-based world.

## Pillars
1. Survival (hunger, thirst, exposure)  2. Crafting depth & player economy
3. Server-authoritative simulation (10Hz tick)  4. Text-first client → GUI later

## Early Loop
Explore → Forage → Craft (hand axe, campfire, water container) → Shelter → Trade.


```markdown
# Game Design Document (Slice: Core TUI & FOV)

## Controls (TUI)
- Movement: arrows / vi (h,j,k,l,y,u,b,n) / numpad
- Wait: `.` or `5`
- Quit: `Esc`
- Hold to move: repeats after initial delay

## View
- 100×40 console; outer border
- Map pane with centered player (clamped near edges)
- Right sidebar: POS, speed, APS, energy, ETA
- Bottom log: recent messages

## Visibility
- Rounded FOV with walls visible at edges
- Day/night adjusts radius (see TICKS_AND_TIME)
- Fog of war: explored areas remain dimly drawn

## Near-term HUD additions
- Needs bars: hunger, thirst, exposure
- Inventory summary (count of key items)
