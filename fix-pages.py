#!/usr/bin/env python3
"""
Quick fix: add hamburger CSS, mobile nav, footer, and JS to all HTML pages.
Keep existing inline styles intact.
"""
import os, re, glob

SITE = "/Users/alex/.openclaw/workspace/autosensor-tech"

def prefix(fp):
    # Use root-relative paths (work from any depth)
    return "/"

EXTRA_CSS = """
.hamburger{display:none;flex-direction:column;gap:5px;background:none;border:none;cursor:pointer;padding:8px;z-index:1002;position:relative}
.hamburger span{display:block;width:24px;height:2px;background:#e0e6ed;transition:all .3s;border-radius:2px}
.hamburger--open span:nth-child(1){transform:rotate(45deg) translate(5px,5px)}
.hamburger--open span:nth-child(2){opacity:0}
.hamburger--open span:nth-child(3){transform:rotate(-45deg) translate(5px,-5px)}
.mobile-nav{display:none;position:fixed;top:0;left:0;width:100%;height:100vh;background:rgba(10,22,40,.98);z-index:1001;padding:80px 2rem 2rem;flex-direction:column;gap:.5rem;overflow-y:auto}
.mobile-nav--open{display:flex}
.mobile-nav__link{color:#e0e6ed;text-decoration:none;padding:.7rem 0;font-size:1.05rem;border-bottom:1px solid rgba(255,255,255,.08);display:block}
.mobile-nav__link:hover{color:#00d4ff}
.mobile-nav__sub{padding-left:1rem}
.mobile-nav__sub .mobile-nav__link{font-size:.9rem;color:#8899aa;border-bottom:none;padding:.4rem 0}
.back-to-top{position:fixed;bottom:2rem;right:2rem;width:44px;height:44px;border-radius:50%;background:#00d4ff;color:#0a1628;border:none;font-size:1.2rem;cursor:pointer;opacity:0;visibility:hidden;transition:all .3s;z-index:999;display:flex;align-items:center;justify-content:center;font-weight:bold}
.back-to-top--visible{opacity:1;visibility:visible}
.footer{background:#1a2d4a;padding:2.5rem 2rem 1.5rem;text-align:center;border-top:1px solid rgba(0,212,255,.2);margin-top:3rem}
.footer p{color:#8899aa;font-size:.85rem}
.footer a{color:#aab8c8;text-decoration:none;margin:0 .6rem;font-size:.85rem;transition:color .2s}
.footer a:hover{color:#00d4ff}
.footer__inner{max-width:1200px;margin:0 auto}
.footer__links{display:flex;justify-content:center;gap:.5rem;margin-bottom:1.5rem;flex-wrap:wrap}
.footer__bottom{padding-top:1rem;border-top:1px solid rgba(255,255,255,.06)}
@media(max-width:768px){
  .hamburger{display:flex}
  .nav-links,.nav__list,.nav{display:none!important}
  .lang-switch{top:10px!important}
}
"""

def mobile_nav(p):
    return f'''
  <div class="mobile-nav">
    <a href="{p}" class="mobile-nav__link">Home</a>
    <a href="{p}technology/" class="mobile-nav__link">C-UAS Technology</a>
    <div class="mobile-nav__sub">
      <a href="{p}technology/#detection" class="mobile-nav__link">↳ Detection</a>
      <a href="{p}technology/#identification" class="mobile-nav__link">↳ Identification</a>
      <a href="{p}technology/#tracking" class="mobile-nav__link">↳ Tracking</a>
      <a href="{p}technology/#defeat" class="mobile-nav__link">↳ Defeat</a>
    </div>
    <a href="{p}solutions/" class="mobile-nav__link">Solutions</a>
    <a href="{p}fpv/" class="mobile-nav__link">FPV Guide</a>
    <a href="{p}knowledge-base/" class="mobile-nav__link">Knowledge Base</a>
    <div class="mobile-nav__sub">
      <a href="{p}knowledge-base/fpv-basics/" class="mobile-nav__link">↳ FPV Basics</a>
      <a href="{p}knowledge-base/components/" class="mobile-nav__link">↳ Components</a>
      <a href="{p}knowledge-base/video-systems/" class="mobile-nav__link">↳ Video Systems</a>
      <a href="{p}knowledge-base/military/" class="mobile-nav__link">↳ Military FPV</a>
      <a href="{p}knowledge-base/c-uas-tech/" class="mobile-nav__link">↳ C-UAS Tech</a>
    </div>
    <a href="{p}products/" class="mobile-nav__link">Products</a>
    <a href="{p}news/" class="mobile-nav__link">News</a>
    <a href="{p}contact/" class="mobile-nav__link">Contact</a>
    <div style="margin-top:1.5rem"><a href="{p}ru/" class="mobile-nav__link" style="color:#667;font-size:.85rem">🌐 Русский</a></div>
  </div>'''

def footer(p):
    return f'''
  <button class="back-to-top" aria-label="Back to top">↑</button>
  <footer class="footer"><div class="footer__inner">
    <div class="footer__links">
      <a href="{p}technology/">Technology</a>
      <a href="{p}solutions/">Solutions</a>
      <a href="{p}knowledge-base/">Knowledge</a>
      <a href="{p}products/">Products</a>
      <a href="{p}fpv/">FPV</a>
      <a href="{p}news/">News</a>
      <a href="{p}contact/">Contact</a>
    </div>
    <div class="footer__bottom"><p>&copy; 2026 AutoSensor Tech</p></div>
  </div></footer>'''

JS = '''<script>
(function(){
  var h=document.querySelector('.hamburger'),m=document.querySelector('.mobile-nav');
  if(h&&m){h.onclick=function(){h.classList.toggle('hamburger--open');m.classList.toggle('mobile-nav--open');document.body.style.overflow=m.classList.contains('mobile-nav--open')?'hidden':''};m.querySelectorAll('.mobile-nav__link').forEach(function(a){a.onclick=function(){h.classList.remove('hamburger--open');m.classList.remove('mobile-nav--open');document.body.style.overflow=''}})}
  var b=document.querySelector('.back-to-top');
  if(b){window.addEventListener('scroll',function(){b.classList.toggle('back-to-top--visible',window.scrollY>300)},{passive:true});b.onclick=function(){window.scrollTo({top:0,behavior:'smooth'})}}
})();
</script>'''

HAMBURGER_BTN = '<button class="hamburger" aria-label="Menu"><span></span><span></span><span></span></button>'

def process(fp):
    with open(fp, 'r', encoding='utf-8') as f:
        c = f.read()
    p = prefix(fp)
    rel = os.path.relpath(fp, SITE)

    # Skip already done
    if 'class="hamburger"' in c and 'class="mobile-nav"' in c and 'class="footer"' in c:
        print(f"  OK: {rel}")
        return False
    print(f"  FIX: {rel}")

    # 1. Extra CSS - append to existing <style> or create before </head>
    if '<style>' in c:
        c = c.replace('</style>', EXTRA_CSS + '</style>', 1)
    else:
        c = c.replace('</head>', f'<style>{EXTRA_CSS}</style>\n</head>', 1)

    # 2. Hamburger button - insert before </nav> or before end of first nav container
    if 'class="hamburger"' not in c:
        # Try </nav> first
        if '</nav>' in c:
            c = c.replace('</nav>', HAMBURGER_BTN + '\n    </nav>', 1)
        # Try closing div after nav-links
        elif '</div>\n        </nav>' in c:
            c = c.replace('</div>\n        </nav>', '</div>\n        ' + HAMBURGER_BTN + '\n    </nav>', 1)
        elif '</div>\n    </nav>' in c:
            c = c.replace('</div>\n    </nav>', '</div>\n    ' + HAMBURGER_BTN + '\n  </nav>', 1)
        # Last resort: after </header>
        elif '</header>' in c:
            c = c.replace('</header>', '  ' + HAMBURGER_BTN + '\n  </header>', 1)

    # 3. Mobile nav - insert after </nav> or </header>
    if 'class="mobile-nav"' not in c:
        mn = mobile_nav(p)
        if '</nav>' in c:
            c = c.replace('</nav>', '</nav>' + mn, 1)
        elif '</header>' in c:
            c = c.replace('</header>', '</header>' + mn, 1)

    # 4. Footer + JS - insert before </body>
    if 'class="footer"' not in c:
        c = c.replace('</body>', footer(p) + JS + '\n</body>', 1)

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(c)
    return True

count = 0
for root, dirs, files in os.walk(SITE):
    dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('css', 'js', '.git')]
    for f in sorted(files):
        if f.endswith('.html'):
            if process(os.path.join(root, f)):
                count += 1
print(f"\nUpdated {count} files")
