#!/usr/bin/env python3
"""Option B transformation: consolidate Learn into Practice, add dedicated Journal tab."""
import re

with open('/home/user/smartypants/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

def find_div_end(text, start):
    """Find end position (exclusive) of the div opening at index start."""
    tag_end = text.index('>', start) + 1
    depth = 1
    pos = tag_end
    while pos < len(text) and depth > 0:
        o = text.find('<div', pos)
        c = text.find('</div>', pos)
        if c == -1:
            break
        if o != -1 and o < c:
            depth += 1
            pos = o + 4
        else:
            depth -= 1
            if depth == 0:
                return c + 6
            pos = c + 6
    return -1

def extract_lp_body(html, lp_id):
    """Return inner content of the tool-body div inside the named lp-pane."""
    pane_start = html.find(f'<div id="{lp_id}" class="lp-pane">')
    if pane_start == -1:
        raise ValueError(f'lp-pane {lp_id} not found')
    # Find tool-body after pane start
    body_start = html.find('<div class="tool-body">', pane_start)
    if body_start == -1:
        raise ValueError(f'tool-body not found in {lp_id}')
    body_end = find_div_end(html, body_start)
    body_open_end = html.index('>', body_start) + 1
    return html[body_open_end : body_end - 6]  # strip outer <div> and </div>

def extract_full_card(html, lp_id):
    """Return the full tool-card div inside the named lp-pane."""
    pane_start = html.find(f'<div id="{lp_id}" class="lp-pane">')
    if pane_start == -1:
        raise ValueError(f'lp-pane {lp_id} not found')
    # Find first <div class="tool-card inside pane
    card_start = html.find('<div class="tool-card"', pane_start)
    if card_start == -1:
        raise ValueError(f'tool-card not found in {lp_id}')
    card_end = find_div_end(html, card_start)
    return html[card_start:card_end]

def remove_worksheet_link(body_html):
    """Remove the 'Open worksheet' tool-use-link from body content."""
    # Remove the last <div class="tool-use-link">...</div> block (the "Open X" link)
    pattern = r'\s*<div class="tool-use-link">\s*<a href="[^"]*" onclick="[^"]*scrollToId[^"]*"[^>]*>[^<]*</a>\s*</div>'
    return re.sub(pattern, '', body_html)

def remove_goal_tracker_link(body_html):
    """Remove the inline 'Open Goal Tracker' link that appears at the top of lp-goals body."""
    pattern = r'\s*<p style="margin:8px 0 0;"><a href="[^"]*goals-worksheet[^"]*"[^>]*>[^<]*</a></p>'
    return re.sub(pattern, '', body_html)

print("Extracting lp-pane bodies...")

# ---- Guide bodies for primers (worksheet-paired guides) ----
body_cba       = remove_worksheet_link(extract_lp_body(content, 'lp-cba'))
body_values    = remove_worksheet_link(extract_lp_body(content, 'lp-values'))
body_change    = remove_worksheet_link(extract_lp_body(content, 'lp-change-plan'))
body_abc       = remove_worksheet_link(extract_lp_body(content, 'lp-abc'))
body_five_q    = remove_worksheet_link(extract_lp_body(content, 'lp-five-q'))
body_wheel     = remove_worksheet_link(extract_lp_body(content, 'lp-wheel'))
body_goals     = remove_goal_tracker_link(remove_worksheet_link(extract_lp_body(content, 'lp-goals')))

# ---- Full cards for reference panes (guide-only) ----
card_self  = extract_full_card(content, 'lp-self-compassion')
card_dents = extract_full_card(content, 'lp-dents')
card_pers  = extract_full_card(content, 'lp-personify')
card_bound = extract_full_card(content, 'lp-boundaries')
card_think = extract_full_card(content, 'lp-thinking-styles')
card_disp  = extract_full_card(content, 'lp-dispute')
card_purs  = extract_full_card(content, 'lp-pursuits')

print("All extractions successful.")

def make_primer(guide_body):
    return f'''
      <details class="ws-primer">
        <summary class="ws-primer-summary">Read the guide</summary>
        <div class="ws-primer-body">{guide_body}
        </div>
      </details>'''

def make_ref_pane(pane_id, full_card):
    return f'''
      <div id="wsPane-{pane_id}" class="ws-pane">
{full_card}
      </div>'''

# ============================================================
# 1. NAV BAR: Learn → Journal, Worksheets → Practice
# ============================================================
content = content.replace(
    "onclick=\"showPage('page-learn');closeLearnCard()\" data-page=\"page-learn\"",
    "onclick=\"showPage('page-journal')\" data-page=\"page-journal\""
)
# Replace book icon + "Learn" label with edit/pencil icon + "Journal"
content = content.replace(
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>\n      Learn',
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>\n      Journal'
)
# Replace clipboard icon + "Worksheets" with same icon + "Practice" in nav
old_ws_nav = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
              'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
              '<path d="M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2"/>'
              '<rect x="9" y="3" width="6" height="4" rx="1"/>'
              '<line x1="9" y1="12" x2="15" y2="12"/>'
              '<line x1="9" y1="16" x2="13" y2="16"/></svg>\n      Worksheets')
new_ws_nav = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
              'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
              '<path d="M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2"/>'
              '<rect x="9" y="3" width="6" height="4" rx="1"/>'
              '<line x1="9" y1="12" x2="15" y2="12"/>'
              '<line x1="9" y1="16" x2="13" y2="16"/></svg>\n      Practice')
content = content.replace(old_ws_nav, new_ws_nav)
print("1. Nav changes done.")

# ============================================================
# 2. RIGHT NOW: remove 4 "Read the guide in Learn" links
# ============================================================
for lp_id in ['lp-halt', 'lp-urge-log', 'lp-breathing', 'lp-urge-surfing']:
    # Pattern:  <div class="tool-use-link">\n        <a ...openLearnCard('lp-xxx')...>...</a>\n      </div>
    pattern = (r'[ \t]*<div class="tool-use-link">\s*'
               r'<a href="javascript:void\(0\)" onclick="showPage\(\'page-learn\'\);'
               rf'openLearnCard\(\'{re.escape(lp_id)}\'\);return false;">&#8594; Read the guide in Learn</a>'
               r'\s*</div>')
    new_content = re.sub(pattern, '', content)
    if new_content == content:
        print(f"  WARNING: tool-use-link for {lp_id} not found!")
    else:
        content = new_content
print("2. Right Now cross-reference links removed.")

# ============================================================
# 3. RIGHT NOW: remove journal card
# ============================================================
# The journal card starts with <!-- JOURNAL --> and ends before </div>\n\n  </div>\n</div>
old_journal_card = '''    <!-- JOURNAL -->
    <div class="tool-card" id="journal" style="margin-top:20px;">
      <div class="tool-card-header">
        <span class="tool-type type-tool">Journal</span>
        <div class="tool-name">Free Write</div>
      </div>
      <div class="tool-body">
        <p style="font-size:13.5px;color:var(--md-on-surface-variant);margin-bottom:12px;">No prompts, no structure — just write. Getting thoughts out of your head reduces emotional load and creates distance from urges.</p>
        <textarea id="journalText" rows="4" placeholder="What\'s on your mind right now?"
          style="width:100%;box-sizing:border-box;margin:0 0 10px;padding:9px 11px;border:1px solid var(--md-outline-variant);border-radius:8px;background:var(--md-surface-container);color:var(--md-on-surface);font-size:13.5px;resize:vertical;font-family:var(--md-font-body);"></textarea>
        <button class="btn-primary" onclick="saveJournalEntry()">Save Entry</button>
        <div id="journalList" style="margin-top:16px;"></div>
      </div>
    </div>'''
if old_journal_card in content:
    content = content.replace(old_journal_card, '')
    print("3. Journal card removed from Right Now.")
else:
    print("  WARNING: Journal card not found in expected location!")

# ============================================================
# 4. WORKSHEET DIRECTORY: rename header, add Reference section
# ============================================================
old_ws_header = ('        <div style="font-size:22px;font-weight:700;letter-spacing:-0.3px;'
                 'color:var(--md-on-surface);">Worksheets</div>\n'
                 '        <div style="font-size:13px;color:var(--md-on-surface-variant);margin-top:4px;">'
                 'Select a worksheet to open it</div>')
new_ws_header = ('        <div style="font-size:22px;font-weight:700;letter-spacing:-0.3px;'
                 'color:var(--md-on-surface);">Practice</div>\n'
                 '        <div style="font-size:13px;color:var(--md-on-surface-variant);margin-top:4px;">'
                 'Worksheets and reference guides for all four SMART points</div>')
if old_ws_header in content:
    content = content.replace(old_ws_header, new_ws_header)
    print("4a. Worksheet directory header renamed.")
else:
    print("  WARNING: ws-index header not found!")

# Add Reference section at end of ws-index (before closing </div>\n    </div>)
ref_rows = '''
      <div class="ws-group-header">Reference &middot; Guides &amp; Practices</div>
      <div class="ws-index-list">
        <button class="ws-index-row" onclick="openWorksheet('self-compassion')">
          <span class="tool-type type-sheet ws-row-badge">Practice</span>
          <div class="ws-row-text">
            <div class="ws-row-name">Practice Self-Compassion</div>
            <div class="ws-row-desc">Meet hard moments with care instead of shame or self-attack</div>
          </div>
          <span class="ws-row-arrow" aria-hidden="true">›</span>
        </button>
        <button class="ws-index-row" onclick="openWorksheet('dents')">
          <span class="tool-type type-guide ws-row-badge">Framework</span>
          <div class="ws-row-text">
            <div class="ws-row-name">Put DENTS in Your Urges</div>
            <div class="ws-row-desc">A five-step acronym for managing active urges in the moment</div>
          </div>
          <span class="ws-row-arrow" aria-hidden="true">›</span>
        </button>
        <button class="ws-index-row" onclick="openWorksheet('personify')">
          <span class="tool-type type-sheet ws-row-badge">Practice</span>
          <div class="ws-row-text">
            <div class="ws-row-name">Personify and Disarm</div>
            <div class="ws-row-desc">Name your urge, identify its scripts, and talk back to reclaim control</div>
          </div>
          <span class="ws-row-arrow" aria-hidden="true">›</span>
        </button>
        <button class="ws-index-row" onclick="openWorksheet('boundaries')">
          <span class="tool-type type-guide ws-row-badge">Tool</span>
          <div class="ws-row-text">
            <div class="ws-row-name">Setting Healthy Boundaries</div>
            <div class="ws-row-desc">Protect your time, energy, and recovery with clear communication</div>
          </div>
          <span class="ws-row-arrow" aria-hidden="true">›</span>
        </button>
        <button class="ws-index-row" onclick="openWorksheet('thinking-styles')">
          <span class="tool-type type-guide ws-row-badge">Reference</span>
          <div class="ws-row-text">
            <div class="ws-row-name">Unhelpful Thinking Styles</div>
            <div class="ws-row-desc">Quick-reference guide to the eight most common cognitive distortions</div>
          </div>
          <span class="ws-row-arrow" aria-hidden="true">›</span>
        </button>
        <button class="ws-index-row" onclick="openWorksheet('dispute')">
          <span class="tool-type type-guide ws-row-badge">Guide</span>
          <div class="ws-row-text">
            <div class="ws-row-name">Dispute Unhelpful Beliefs</div>
            <div class="ws-row-desc">Identify belief patterns and replace them with more helpful thinking</div>
          </div>
          <span class="ws-row-arrow" aria-hidden="true">›</span>
        </button>
        <button class="ws-index-row" onclick="openWorksheet('pursuits')">
          <span class="tool-type type-guide ws-row-badge">Guide</span>
          <div class="ws-row-text">
            <div class="ws-row-name">Explore New Pursuits and Passions</div>
            <div class="ws-row-desc">Find what can genuinely replace the functions addictive behavior served</div>
          </div>
          <span class="ws-row-arrow" aria-hidden="true">›</span>
        </button>
      </div>'''

# Insert reference rows before the end of ws-index
old_index_end = '      </div>\n    </div>\n\n    <!-- Worksheet Detail View -->'
new_index_end = '      </div>' + ref_rows + '\n    </div>\n\n    <!-- Worksheet Detail View -->'
if old_index_end in content:
    content = content.replace(old_index_end, new_index_end)
    print("4b. Reference rows added to directory.")
else:
    print("  WARNING: ws-index end marker not found!")

# ============================================================
# 5. BACK BUTTON: "Back to Worksheets" → "Back to Practice"
# ============================================================
content = content.replace(
    '&#8592; Back to Worksheets',
    '&#8592; Back to Practice'
)
print("5. Back button label updated.")

# ============================================================
# 6. WORKSHEET PANES: remove "Read the guide in Learn" links
#    and add collapsible primers
# ============================================================
ws_primer_map = [
    ('cba',              body_cba,    'lp-cba'),
    ('values',           body_values, 'lp-values'),
    ('change-plan',      body_change, 'lp-change-plan'),
    ('abc',              body_abc,    'lp-abc'),
    ('five-q',           body_five_q, 'lp-five-q'),
    ('wheel',            body_wheel,  'lp-wheel'),
    ('goals-worksheet',  body_goals,  'lp-goals'),
]

for ws_id, primer_body, lp_id in ws_primer_map:
    # Remove "Read the guide in Learn" link from worksheet pane
    pattern = (r'[ \t]*<div class="tool-use-link">\s*'
               r'<a href="javascript:void\(0\)" onclick="showPage\(\'page-learn\'\);'
               rf'openLearnCard\(\'{re.escape(lp_id)}\'\);return false;">&#8594; Read the guide in Learn</a>'
               r'\s*</div>')
    new_content = re.sub(pattern, '', content)
    if new_content == content:
        print(f"  WARNING: ws learn link not removed for {ws_id}!")
    content = new_content

    # Add primer before the closing </div> of this ws-pane
    # Each ws-pane ends with unique closing sequence - anchor on the pane's closing
    # We find the wsPane-XXX div, find its end, and insert primer before it
    pane_marker = f'<div id="wsPane-{ws_id}" class="ws-pane">'
    pane_start = content.find(pane_marker)
    if pane_start == -1:
        print(f"  WARNING: wsPane-{ws_id} not found!")
        continue
    pane_end = find_div_end(content, pane_start)
    if pane_end == -1:
        print(f"  WARNING: could not find end of wsPane-{ws_id}!")
        continue
    # pane_end points just after the closing </div>
    # Insert primer before that closing </div>
    insert_pos = pane_end - 6  # back up 6 chars = len('</div>')
    primer_html = make_primer(primer_body)
    content = content[:insert_pos] + primer_html + '\n' + content[insert_pos:]
    print(f"  Primer added to wsPane-{ws_id}.")

print("6. Worksheet pane primers inserted.")

# ============================================================
# 7. NEW REFERENCE WS-PANES (7 guide-only entries)
# ============================================================
ref_panes_html = ''
ref_pane_map = [
    ('self-compassion',  card_self),
    ('dents',            card_dents),
    ('personify',        card_pers),
    ('boundaries',       card_bound),
    ('thinking-styles',  card_think),
    ('dispute',          card_disp),
    ('pursuits',         card_purs),
]
for pane_id, full_card in ref_pane_map:
    ref_panes_html += make_ref_pane(pane_id, full_card) + '\n'

# Insert after the last existing ws-pane (goals-worksheet), before ws-view closing </div>
# The ws-view ends with: [last ws-pane closing] then </div>\n\n  </div>\n</div>
old_wsview_end = '    </div>\n\n  </div>\n</div>\n\n<!-- ═══ PAGE: LEARN'
new_wsview_end = ref_panes_html + '\n    </div>\n\n  </div>\n</div>\n\n<!-- ═══ PAGE: LEARN'
if old_wsview_end in content:
    content = content.replace(old_wsview_end, new_wsview_end)
    print("7. Reference ws-panes added.")
else:
    # Try alternative ending
    old_wsview_end2 = '    </div>\n\n  </div>\n</div><!-- /page-worksheets'
    if old_wsview_end2 not in content:
        # Try to find the ws-view closing differently
        print("  WARNING: ws-view end marker not found, searching...")
        idx = content.find('<!-- ═══ PAGE: LEARN')
        if idx != -1:
            # Insert before page-learn
            content = content[:idx] + ref_panes_html + '\n    </div>\n\n  </div>\n</div>\n\n' + content[idx:]
            print("  Used fallback: inserted before page-learn comment.")
        else:
            print("  ERROR: Could not find insertion point for reference panes!")

# ============================================================
# 8. REPLACE PAGE-LEARN WITH PAGE-JOURNAL
# ============================================================
# Find the full page-learn block
page_learn_start = content.find('<div class="page" id="page-learn">')
page_learn_end_marker = '</div><!-- /page-learn -->'
page_learn_end_idx = content.find(page_learn_end_marker)
if page_learn_start != -1 and page_learn_end_idx != -1:
    page_learn_end_idx += len(page_learn_end_marker)
    page_journal_html = '''<div class="page" id="page-journal">
  <div class="container">
    <div style="padding-top:28px;padding-bottom:4px;">
      <div style="font-size:22px;font-weight:700;letter-spacing:-0.3px;color:var(--md-on-surface);">Journal</div>
      <div style="font-size:13px;color:var(--md-on-surface-variant);margin-top:4px;">Your private space to write freely</div>
    </div>

    <div class="tool-card" style="margin-top:16px;">
      <div class="tool-card-header">
        <span class="tool-type type-tool">Free Write</span>
        <div class="tool-name">New Entry</div>
      </div>
      <div class="tool-body">
        <p style="font-size:13.5px;color:var(--md-on-surface-variant);margin-bottom:12px;">No prompts, no structure — just write. Getting thoughts out of your head reduces emotional load and creates distance from urges.</p>
        <textarea id="journalText" rows="5" placeholder="What&#39;s on your mind right now?"
          style="width:100%;box-sizing:border-box;margin:0 0 10px;padding:9px 11px;border:1px solid var(--md-outline-variant);border-radius:8px;background:var(--md-surface-container);color:var(--md-on-surface);font-size:13.5px;resize:vertical;font-family:var(--md-font-body);"></textarea>
        <button class="btn-primary" onclick="saveJournalEntry()">Save Entry</button>
      </div>
    </div>

    <div style="margin-top:24px;">
      <div class="ws-group-header">Past Entries</div>
      <div id="journalList"></div>
    </div>

  </div>
</div><!-- /page-journal -->'''
    content = content[:page_learn_start] + page_journal_html + content[page_learn_end_idx:]
    print("8. page-learn replaced with page-journal.")
else:
    print("  ERROR: page-learn block not found!")

# ============================================================
# 9. CSS: add ws-primer styles (insert after .lp-pane rules)
# ============================================================
ws_primer_css = '''
  /* ══ WS-PRIMER (collapsible guide background) ═════════════ */
  .ws-primer {
    margin-top: 12px;
    border: 1px solid var(--md-outline-variant);
    border-radius: var(--md-shape-md);
    overflow: hidden;
    background: var(--md-surface-container-low);
  }
  .ws-primer-summary {
    display: flex; align-items: center; gap: 8px;
    padding: 12px 20px;
    cursor: pointer; list-style: none;
    font-size: 13px; font-weight: 600; letter-spacing: 0.01em;
    color: var(--md-on-surface-variant);
    transition: background var(--md-dur-short) var(--md-easing-standard);
  }
  .ws-primer-summary::-webkit-details-marker { display: none; }
  .ws-primer-summary::before { content: "›"; font-size: 17px; line-height: 1; transition: transform var(--md-dur-short) var(--md-easing-standard); }
  .ws-primer[open] > .ws-primer-summary::before { transform: rotate(90deg); }
  .ws-primer[open] > .ws-primer-summary { border-bottom: 1px solid var(--md-outline-variant); }
  .ws-primer-summary:hover { background: color-mix(in srgb, var(--md-on-surface) 8%, transparent); }
  .ws-primer-body { padding: 4px 20px 16px; }
  .ws-primer-body .tool-summary { margin-top: 14px; }
'''

css_insert_anchor = '  .lp-pane { display: none; }\n  .lp-pane.lp-pane-active { display: block; }'
if css_insert_anchor in content:
    content = content.replace(css_insert_anchor, css_insert_anchor + ws_primer_css)
    print("9. ws-primer CSS added.")
else:
    print("  WARNING: CSS anchor not found!")

# ============================================================
# 10. JS UPDATES
# ============================================================
# 10a. PAGE_IDS: replace 'page-learn' with 'page-journal'
content = content.replace(
    "var PAGE_IDS = ['page-rightnow', 'page-worksheets', 'page-progress', 'page-learn', 'page-slip', 'page-settings'];",
    "var PAGE_IDS = ['page-rightnow', 'page-worksheets', 'page-progress', 'page-journal', 'page-slip', 'page-settings'];"
)
print("10a. PAGE_IDS updated.")

# 10b. TOOL_PAGE_MAP: update all learn references → worksheets/journal
old_tpm = '''var TOOL_PAGE_MAP = {
  'halt': 'page-rightnow', 'urge-log': 'page-rightnow', 'urge-history': 'page-progress',
  'breathing': 'page-rightnow', 'urge-surfing': 'page-rightnow', 'journal': 'page-rightnow',
  'cba': 'page-worksheets', 'abc': 'page-worksheets', 'five-q': 'page-worksheets',
  'values': 'page-worksheets', 'change-plan': 'page-worksheets', 'wheel': 'page-worksheets',
  'dents': 'page-learn', 'personify': 'page-learn', 'boundaries': 'page-learn',
  'thinking-styles': 'page-learn', 'dispute': 'page-learn',
  'self-compassion': 'page-learn', 'goals': 'page-learn', 'pursuits': 'page-learn',
  'resources': 'page-learn', 'point1': 'page-learn', 'point2': 'page-learn',
  'point3': 'page-learn', 'point4': 'page-learn',
  'tracker': 'page-progress',
  'lapse': 'page-slip',
  'page-rightnow': 'page-rightnow', 'page-worksheets': 'page-worksheets',
  'page-progress': 'page-progress', 'page-learn': 'page-learn', 'page-slip': 'page-slip',
  'page-settings': 'page-settings'
};'''
new_tpm = '''var TOOL_PAGE_MAP = {
  'halt': 'page-rightnow', 'urge-log': 'page-rightnow', 'urge-history': 'page-progress',
  'breathing': 'page-rightnow', 'urge-surfing': 'page-rightnow',
  'cba': 'page-worksheets', 'abc': 'page-worksheets', 'five-q': 'page-worksheets',
  'values': 'page-worksheets', 'change-plan': 'page-worksheets', 'wheel': 'page-worksheets',
  'goals-worksheet': 'page-worksheets', 'goals': 'page-worksheets',
  'dents': 'page-worksheets', 'personify': 'page-worksheets', 'boundaries': 'page-worksheets',
  'thinking-styles': 'page-worksheets', 'dispute': 'page-worksheets',
  'self-compassion': 'page-worksheets', 'pursuits': 'page-worksheets',
  'journal': 'page-journal',
  'tracker': 'page-progress',
  'lapse': 'page-slip',
  'page-rightnow': 'page-rightnow', 'page-worksheets': 'page-worksheets',
  'page-progress': 'page-progress', 'page-journal': 'page-journal', 'page-slip': 'page-slip',
  'page-settings': 'page-settings'
};'''
if old_tpm in content:
    content = content.replace(old_tpm, new_tpm)
    print("10b. TOOL_PAGE_MAP updated.")
else:
    print("  WARNING: TOOL_PAGE_MAP not found verbatim, trying regex...")
    content = re.sub(r'var TOOL_PAGE_MAP = \{[^}]+\};', new_tpm, content, flags=re.DOTALL)
    print("10b. TOOL_PAGE_MAP updated via regex.")

# 10c. _WS_IDS: add 7 reference pane IDs
old_ws_ids = "var _WS_IDS = ['cba','values','change-plan','abc','five-q','wheel','goals-worksheet'];"
new_ws_ids = ("var _WS_IDS = ['cba','values','change-plan','abc','five-q','wheel','goals-worksheet',"
              "'self-compassion','dents','personify','boundaries','thinking-styles','dispute','pursuits'];")
if old_ws_ids in content:
    content = content.replace(old_ws_ids, new_ws_ids)
    print("10c. _WS_IDS updated.")
else:
    print("  WARNING: _WS_IDS not found!")

# 10d. scrollToId: update wsIds list to match _WS_IDS and remove lpMap
old_scroll = """function scrollToId(id) {
  var wsIds = ['cba','values','change-plan','abc','five-q','wheel','goals-worksheet'];
  if (wsIds.indexOf(id) !== -1) { openWorksheet(id); return; }
  var lpMap = {
    'self-compassion':'lp-self-compassion','dents':'lp-dents','personify':'lp-personify',
    'boundaries':'lp-boundaries','thinking-styles':'lp-thinking-styles','dispute':'lp-dispute',
    'self-compassion':'lp-self-compassion','goals':'lp-goals','pursuits':'lp-pursuits'
  };
  if (lpMap[id]) { openLearnCard(lpMap[id]); return; }
  setTimeout(function() {
    var el = document.getElementById(id);
    if (el) el.scrollIntoView({ block: 'start' });
  }, 50);
}"""
new_scroll = """function scrollToId(id) {
  if (_WS_IDS.indexOf(id) !== -1) { openWorksheet(id); return; }
  setTimeout(function() {
    var el = document.getElementById(id);
    if (el) el.scrollIntoView({ block: 'start' });
  }, 50);
}"""
if old_scroll in content:
    content = content.replace(old_scroll, new_scroll)
    print("10d. scrollToId updated.")
else:
    print("  WARNING: scrollToId not found verbatim!")

# 10e. Remove _LP_IDS, openLearnCard, closeLearnCard (replace with stubs for safety)
old_lp_section = """var _LP_IDS = [
  'lp-cba','lp-values','lp-change-plan','lp-self-compassion',
  'lp-halt','lp-urge-log','lp-dents','lp-breathing',
  'lp-personify','lp-urge-surfing','lp-boundaries',
  'lp-thinking-styles','lp-abc','lp-dispute','lp-five-q',
  'lp-wheel','lp-goals','lp-pursuits'
];

function openLearnCard(id) {
  var idx = document.getElementById('lpIndex');
  var view = document.getElementById('lpView');
  if (!idx || !view) return;
  idx.style.display = 'none';
  view.style.display = '';
  _LP_IDS.forEach(function(lid) {
    var p = document.getElementById(lid);
    if (p) p.classList.toggle('lp-pane-active', lid === id);
  });
  view.scrollIntoView({ block: 'start' });
}

function closeLearnCard() {
  var idx = document.getElementById('lpIndex');
  var view = document.getElementById('lpView');
  if (!idx || !view) return;
  view.style.display = 'none';
  _LP_IDS.forEach(function(lid) {
    var p = document.getElementById(lid);
    if (p) p.classList.remove('lp-pane-active');
  });
  idx.style.display = '';
  idx.scrollIntoView({ block: 'start' });
}"""
if old_lp_section in content:
    content = content.replace(old_lp_section, '')
    print("10e. _LP_IDS / openLearnCard / closeLearnCard removed.")
else:
    print("  WARNING: _LP_IDS section not found verbatim!")

# 10f. renderJournal: update getElementById to look for journalList in page-journal
# The function targets 'journalList' which will now be in page-journal — no change needed
# since it's a standard getElementById call. Just verify the DOMContentLoaded call.
# Remove the standalone renderJournal DOMContentLoaded call (it will be called from initPage)
# Actually, keep it — renderJournal reads from localStorage, will work fine from any page state.

# 10g. TOOL_PAGE_MAP entry for 'journal' — already done in 10b.
# 'journal' key links to 'page-journal' now.

print("10. JS updates complete.")

# ============================================================
# 11. APP_VERSION: bump to 2.4.2
# ============================================================
content = content.replace("var APP_VERSION = '2.4.1';", "var APP_VERSION = '2.4.2';")
print("11. APP_VERSION bumped to 2.4.2.")

# ============================================================
# WRITE OUTPUT
# ============================================================
with open('/home/user/smartypants/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\nTransformation complete. index.html written.")
