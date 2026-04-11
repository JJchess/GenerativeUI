---
name: generative_ui
description: Route visualization requests to read_me and show_widget tools.
always: true
---

For visual requests, call visualize_read_me first with the minimum relevant modules,
then call show_widget with i_have_seen_read_me=true.
Use one widget_type from interactive/chart/chart_interactive/mockup/art/art_interactive/diagram.
Keep widget_code as a fragment only, avoid doctype/html/body wrappers.
Structure widget_code for streaming: short style first, content HTML next, script last.
Keep explanatory prose in assistant text, not inside widget_code.
