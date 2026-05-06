#!/usr/bin/env python3
"""Add custom accent color picker to smartypants Settings."""

with open('/home/user/smartypants/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ============================================================
# 1. CSS — accent swatch styles (insert after .swatch-name rule)
# ============================================================
accent_css = '''
  /* ══ ACCENT COLOR PICKER ════════════════════════════════════ */
  .accent-row       { display: flex; flex-wrap: wrap; align-items: center; gap: 8px; margin: 10px 0 6px; }
  .accent-swatch    {
    width: 32px; height: 32px; border-radius: 50%; border: 2px solid transparent;
    cursor: pointer; padding: 0; flex-shrink: 0;
    transition: transform var(--md-dur-short) var(--md-easing-standard),
                border-color var(--md-dur-short) var(--md-easing-standard);
    position: relative;
  }
  .accent-swatch:hover  { transform: scale(1.18); }
  .accent-swatch.accent-swatch-active { border-color: var(--md-on-surface); }
  .accent-swatch.accent-swatch-active::after {
    content: "✓"; position: absolute; inset: 0;
    display: flex; align-items: center; justify-content: center;
    font-size: 14px; font-weight: 700; color: #fff;
    text-shadow: 0 1px 3px rgba(0,0,0,0.5);
  }
  .accent-picker-wrap {
    display: flex; align-items: center; gap: 8px;
    padding: 6px 12px; border: 1px solid var(--md-outline-variant);
    border-radius: var(--md-shape-full); background: var(--md-surface-container);
    cursor: pointer;
  }
  .accent-picker-wrap:hover { border-color: var(--md-outline); }
  #accentPicker { width: 22px; height: 22px; border: none; padding: 0; background: none; cursor: pointer; border-radius: 50%; overflow: hidden; }
  .accent-picker-label { font-size: 12px; color: var(--md-on-surface-variant); pointer-events: none; }
  .accent-reset { font-size: 12px; color: var(--md-secondary); background: none; border: none; cursor: pointer; padding: 2px 0; text-decoration: underline; font-family: var(--md-font-body); }
  .accent-reset:hover { color: var(--md-primary); }
'''

css_anchor = '  .theme-swatch.swatch-active .swatch-name { color: var(--md-primary); font-weight: 700; }'
if css_anchor in content:
    content = content.replace(css_anchor, css_anchor + accent_css)
    print("1. Accent CSS added.")
else:
    print("  WARNING: CSS anchor not found!")

# ============================================================
# 2. Fix light-theme swatch dot to show new baseline purple
# ============================================================
content = content.replace(
    'style="background:#FAFAFF;"><div class="swatch-card" style="background:#EEEEF6;"></div><div class="swatch-dot" style="background:#4040C0;">',
    'style="background:#FFFBFE;"><div class="swatch-card" style="background:#F3EDF7;"></div><div class="swatch-dot" style="background:#6750A4;">'
)
print("2. Light theme swatch updated to baseline purple.")

# ============================================================
# 3. HTML — Accent Color section in Settings
#    Insert after the font options, before Reminders section
# ============================================================
accent_html = '''
      <div class="settings-row-label" style="margin-top:18px;margin-bottom:10px;">Accent Color</div>
      <div class="accent-row" id="accentSwatches">
        <button class="accent-swatch" data-color="#6750A4" onclick="applyAccent('#6750A4')" style="background:#6750A4;" title="Purple — MD3 baseline" aria-label="Purple"></button>
        <button class="accent-swatch" data-color="#0061A4" onclick="applyAccent('#0061A4')" style="background:#0061A4;" title="Blue" aria-label="Blue"></button>
        <button class="accent-swatch" data-color="#006A6A" onclick="applyAccent('#006A6A')" style="background:#006A6A;" title="Teal" aria-label="Teal"></button>
        <button class="accent-swatch" data-color="#006E1C" onclick="applyAccent('#006E1C')" style="background:#006E1C;" title="Green" aria-label="Green"></button>
        <button class="accent-swatch" data-color="#7D5700" onclick="applyAccent('#7D5700')" style="background:#7D5700;" title="Amber" aria-label="Amber"></button>
        <button class="accent-swatch" data-color="#9C4146" onclick="applyAccent('#9C4146')" style="background:#9C4146;" title="Red" aria-label="Red"></button>
        <button class="accent-swatch" data-color="#7D3A73" onclick="applyAccent('#7D3A73')" style="background:#7D3A73;" title="Mauve" aria-label="Mauve"></button>
        <button class="accent-swatch" data-color="#3D5A80" onclick="applyAccent('#3D5A80')" style="background:#3D5A80;" title="Navy" aria-label="Navy"></button>
        <label class="accent-picker-wrap" title="Custom color">
          <input type="color" id="accentPicker" value="#6750A4" oninput="applyAccent(this.value)" aria-label="Custom accent color">
          <span class="accent-picker-label">Custom</span>
        </label>
      </div>
      <button class="accent-reset" onclick="resetAccent()">Reset to theme default</button>
'''

# Insert before the Reminders section
html_anchor = '    <div class="settings-section" id="notifSection" style="display:none;">'
if html_anchor in content:
    # Find the end of the Appearance section's inner div (closing before notifSection)
    # The appearance section ends just before notifSection
    insert_before = '    </div>\n\n    <div class="settings-section" id="notifSection"'
    if insert_before in content:
        old_font_end = ('          <button class="font-opt" data-font="aptos"     onclick="applyFont(\'aptos\')"'
                        '      style="font-family:Aptos,\'Segoe UI\',Helvetica,sans-serif;">Aptos</button>\n'
                        '        </div>\n'
                        '      </div>\n'
                        '    </div>')
        new_font_end = ('          <button class="font-opt" data-font="aptos"     onclick="applyFont(\'aptos\')"'
                        '      style="font-family:Aptos,\'Segoe UI\',Helvetica,sans-serif;">Aptos</button>\n'
                        '        </div>\n'
                        '      </div>\n' + accent_html +
                        '    </div>')
        if old_font_end in content:
            content = content.replace(old_font_end, new_font_end)
            print("3. Accent HTML inserted in Settings.")
        else:
            print("  WARNING: font-end anchor not found, trying simpler approach...")
            # Simpler: insert accent_html just before </div>\n\n    <div class="settings-section" id="notifSection"
            content = content.replace(
                '    </div>\n\n    <div class="settings-section" id="notifSection"',
                accent_html + '\n    </div>\n\n    <div class="settings-section" id="notifSection"'
            )
            print("3. Accent HTML inserted via fallback.")
    else:
        print("  WARNING: HTML insert anchor not found!")
else:
    print("  WARNING: notifSection not found!")

# ============================================================
# 4. JS — Full accent color engine
# ============================================================
accent_js = '''
// ══ CUSTOM ACCENT COLOR ENGINE ════════════════════════════

var ACCENT_KEY = 'smart_accent_v1';

// Hex → OKLCH (Ottosson 2020)
function _hexToOklch(hex) {
  var r=parseInt(hex.slice(1,3),16)/255, g=parseInt(hex.slice(3,5),16)/255, b=parseInt(hex.slice(5,7),16)/255;
  function lin(c){ return c<=0.04045?c/12.92:Math.pow((c+0.055)/1.055,2.4); }
  r=lin(r); g=lin(g); b=lin(b);
  var l=Math.cbrt(0.4122214708*r+0.5363325363*g+0.0514459929*b);
  var m=Math.cbrt(0.2119034982*r+0.6806995451*g+0.1073969566*b);
  var s=Math.cbrt(0.0883024619*r+0.2817188376*g+0.6299787005*b);
  var L=0.2104542553*l+0.7936177850*m-0.0040720468*s;
  var A=1.9779984951*l-2.4285922050*m+0.4505937099*s;
  var B=0.0259040371*l+0.7827717662*m-0.8086757660*s;
  var C=Math.sqrt(A*A+B*B);
  var H=Math.atan2(B,A)*180/Math.PI; if(H<0)H+=360;
  return {L:L, C:C, H:H};
}

// HCT tone → OKLCH lightness (perceptual approximation)
var _TONE_L=[[0,0],[10,0.19],[20,0.32],[30,0.43],[40,0.51],[50,0.60],
             [60,0.68],[70,0.77],[80,0.85],[90,0.92],[95,0.96],[99,0.99],[100,1.0]];
function _toneL(t) {
  for(var i=0;i<_TONE_L.length-1;i++){
    if(t>=_TONE_L[i][0]&&t<=_TONE_L[i+1][0]){
      var f=(t-_TONE_L[i][0])/(_TONE_L[i+1][0]-_TONE_L[i][0]);
      return _TONE_L[i][1]+f*(_TONE_L[i+1][1]-_TONE_L[i][1]);
    }
  }
  return t/100;
}

// Build one OKLCH CSS string for a palette at a given tone
function _pt(C, H, tone) {
  var l = _toneL(tone);
  // Chroma tapers symmetrically toward black and white extremes
  var chromaFactor = Math.pow(Math.sin(Math.PI * Math.min(tone,100) / 100), 0.6);
  return 'oklch('+l.toFixed(3)+' '+(C*chromaFactor).toFixed(4)+' '+H.toFixed(1)+')';
}

// Generate the 14 chromatic color-role CSS properties for the active theme
function _accentRoles(seedHex) {
  var ok = _hexToOklch(seedHex);
  var H = ok.H, C = ok.C;
  var dark = !document.documentElement.classList.contains('light');

  // Palettes: primary (seed), secondary (same hue, desaturated),
  //           tertiary (hue +65°, moderate chroma)
  var pC=C,        pH=H;
  var sC=C*0.33,   sH=H;
  var tC=C*0.50,   tH=(H+65)%360;

  if (dark) {
    return {
      '--md-primary':              _pt(pC,pH,80),
      '--md-on-primary':           _pt(pC,pH,20),
      '--md-primary-container':    _pt(pC,pH,30),
      '--md-on-primary-container': _pt(pC,pH,90),
      '--md-secondary':              _pt(sC,sH,80),
      '--md-on-secondary':           _pt(sC,sH,20),
      '--md-secondary-container':    _pt(sC,sH,30),
      '--md-on-secondary-container': _pt(sC,sH,90),
      '--md-tertiary':              _pt(tC,tH,80),
      '--md-on-tertiary':           _pt(tC,tH,20),
      '--md-tertiary-container':    _pt(tC,tH,30),
      '--md-on-tertiary-container': _pt(tC,tH,90),
      '--md-surface-tint':          _pt(pC,pH,80),
      '--md-inverse-primary':       _pt(pC,pH,40)
    };
  } else {
    return {
      '--md-primary':              _pt(pC,pH,40),
      '--md-on-primary':           'oklch(1 0 0)',
      '--md-primary-container':    _pt(pC,pH,90),
      '--md-on-primary-container': _pt(pC,pH,10),
      '--md-secondary':              _pt(sC,sH,40),
      '--md-on-secondary':           'oklch(1 0 0)',
      '--md-secondary-container':    _pt(sC,sH,90),
      '--md-on-secondary-container': _pt(sC,sH,10),
      '--md-tertiary':              _pt(tC,tH,40),
      '--md-on-tertiary':           'oklch(1 0 0)',
      '--md-tertiary-container':    _pt(tC,tH,90),
      '--md-on-tertiary-container': _pt(tC,tH,10),
      '--md-surface-tint':          _pt(pC,pH,40),
      '--md-inverse-primary':       _pt(pC,pH,80)
    };
  }
}

var _ACCENT_PROPS = [
  '--md-primary','--md-on-primary','--md-primary-container','--md-on-primary-container',
  '--md-secondary','--md-on-secondary','--md-secondary-container','--md-on-secondary-container',
  '--md-tertiary','--md-on-tertiary','--md-tertiary-container','--md-on-tertiary-container',
  '--md-surface-tint','--md-inverse-primary'
];

function applyAccent(hex) {
  // Normalize to 7-char hex (color input gives '#rrggbb')
  if (!hex || hex.length < 7) return;
  var roles = _accentRoles(hex);
  var root = document.documentElement;
  Object.keys(roles).forEach(function(k){ root.style.setProperty(k, roles[k]); });
  lsSet(ACCENT_KEY, hex);
  _updateAccentUI(hex);
}

function resetAccent() {
  var root = document.documentElement;
  _ACCENT_PROPS.forEach(function(p){ root.style.removeProperty(p); });
  lsSet(ACCENT_KEY, '');
  _updateAccentUI('');
}

function _updateAccentUI(hex) {
  document.querySelectorAll('.accent-swatch').forEach(function(sw){
    sw.classList.toggle('accent-swatch-active', !!hex && sw.dataset.color.toLowerCase()===hex.toLowerCase());
  });
  var picker = document.getElementById('accentPicker');
  if (picker) picker.value = (hex && hex.length===7) ? hex : '#6750A4';
}

function initAccentColor() {
  var saved = lsGet(ACCENT_KEY);
  if (saved) applyAccent(saved);
  else _updateAccentUI('');
}
'''

# Insert after the closeLearnCard stub / before scrollToId — actually, insert near the
# existing applyTheme / applyFont functions for logical grouping.
# We'll insert just after the updateFontButtons function.
js_anchor = 'function applyTheme(id) {'
if js_anchor in content:
    content = content.replace(js_anchor, accent_js + '\nfunction applyTheme(id) {')
    print("4. Accent JS inserted.")
else:
    print("  WARNING: applyTheme anchor not found!")

# ============================================================
# 5. Hook applyTheme to re-apply accent on theme change
# ============================================================
old_apply_theme = '''function applyTheme(id) {
  _THEME_CLASSES.forEach(function(c) { html.classList.remove(c); });
  html.classList.remove('light');
  if (_LIGHT_THEMES.indexOf(id) !== -1) html.classList.add('light');
  if (id !== 'dark' && id !== 'light') html.classList.add(id);
  lsSet('smartTheme', id);
  updateThemeSwatches(id);
  setTimeout(function() { try { var v = getWheelVals(); drawWheel(v); } catch(e) {} }, 50);
}'''
new_apply_theme = '''function applyTheme(id) {
  _THEME_CLASSES.forEach(function(c) { html.classList.remove(c); });
  html.classList.remove('light');
  if (_LIGHT_THEMES.indexOf(id) !== -1) html.classList.add('light');
  if (id !== 'dark' && id !== 'light') html.classList.add(id);
  lsSet('smartTheme', id);
  updateThemeSwatches(id);
  // Re-apply accent so tones recalculate for the new light/dark variant
  var savedAccent = lsGet(ACCENT_KEY);
  if (savedAccent) applyAccent(savedAccent);
  setTimeout(function() { try { var v = getWheelVals(); drawWheel(v); } catch(e) {} }, 50);
}'''
if old_apply_theme in content:
    content = content.replace(old_apply_theme, new_apply_theme)
    print("5. applyTheme hooked to re-apply accent.")
else:
    print("  WARNING: applyTheme body not matched exactly!")

# ============================================================
# 6. Call initAccentColor on DOMContentLoaded
# ============================================================
old_init = '''document.addEventListener('DOMContentLoaded', function() {
  showPage('page-rightnow');
  initSettingsPage();
});'''
new_init = '''document.addEventListener('DOMContentLoaded', function() {
  showPage('page-rightnow');
  initSettingsPage();
  initAccentColor();
});'''
if old_init in content:
    content = content.replace(old_init, new_init)
    print("6. initAccentColor called on DOMContentLoaded.")
else:
    print("  WARNING: DOMContentLoaded block not found!")

# ============================================================
# 7. APP_VERSION bump to 2.4.3
# ============================================================
content = content.replace("var APP_VERSION = '2.4.2';", "var APP_VERSION = '2.4.3';")
print("7. APP_VERSION bumped to 2.4.3.")

# ============================================================
# WRITE
# ============================================================
with open('/home/user/smartypants/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\nDone. index.html updated.")
