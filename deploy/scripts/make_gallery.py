"""Writes deploy/netlify_site/gallery.html: every picture, video and simulation the tutor can show, by chapter and scenario, with its
alt text and credit, so a faculty reviewer can look at all of them without walking a problem. Read through engine.read_openers (the
same reader the factory uses); links are relative to the site root, so the page works on the deployed site or beside index.html."""
import glob, html, os, sys
sys.path.insert(0, ".")
import engine
out = sys.argv[1] if len(sys.argv) > 1 else "deploy/netlify_site/gallery.html"
rows = ['<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Tutor preview: pictures and simulations</title>',
        '<style>body{font:16px/1.45 system-ui,sans-serif;max-width:900px;margin:24px auto;padding:0 16px;color:#222}h2{margin-top:36px}figure{margin:12px 0;padding:12px;border:1px solid #ddd;border-radius:8px}img,video{max-width:100%;height:auto}figcaption{font-size:14px;color:#555;margin-top:6px}a.sim{display:inline-block;margin:6px 0;padding:6px 10px;border:1px solid #1b5e6e;border-radius:6px;color:#1b5e6e;text-decoration:none}.miss{color:#a00}.credit{font-size:12px;color:#777}</style>',
        '<h1>Pictures and simulations in the tutor</h1><p>Everything the tutor can put on the left of the screen, by scenario. In a run, a picture appears with the opening question or after the particle account, and a simulation opens at the step named. A simulation\'s address carries the problem\'s own numbers; from here it opens with its defaults. <a href="index.html">Back to the tutor</a>.</p>']
def fig(tag, cap, credit=""):
    return f'<figure>{tag}<figcaption>{cap}' + (f'<div class="credit">{html.escape(credit)}</div>' if credit else "") + '</figcaption></figure>'
for f in sorted(glob.glob("content_*_openers.csv")):
    arch = f[len("content_"):-len("_openers.csv")]
    rows.append(f"<h2>{html.escape(arch)}</h2>")
    for o in engine.read_openers(f):
        m = o.get("media") or {}; items = []
        for label, key in (("with the opening question", "image_with_question"), ("after the account is accepted", "image_after_account")):
            p = (m.get(key) or "").strip()
            if not p: continue
            alt = html.escape((m.get("image_alt") or "").strip())
            if p.lower().endswith((".mp4", ".webm", ".mov")): tag = f'<video controls preload="metadata" src="media/{html.escape(p)}" aria-label="{alt}"></video>'
            else: tag = f'<img src="media/{html.escape(p)}" alt="{alt}" onerror="this.outerHTML=\'<p class=miss>Missing on the site: media/{html.escape(p)}</p>\'">'
            items.append(fig(tag, f"<b>Picture {label}</b> (media/{html.escape(p)})<br>{alt}", m.get("credit") or ""))
        s = (m.get("simulation") or "").strip()
        if s:
            items.append(fig(f'<a class="sim" href="media/{html.escape(s.split("?")[0])}" target="_blank">Open the simulation ({html.escape(os.path.basename(s.split("?")[0]))})</a>',
                             f"Opens in a run at: {html.escape(m.get('simulation_opens') or 'the meaning step')}. Address in the tutor: media/{html.escape(s)}"))
        rows.append(f"<h3>{html.escape(o['title'])} <small>({html.escape(o.get('role') or 'floater')})</small></h3>" + ("".join(items) if items else "<p>No picture or simulation.</p>"))
os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
open(out, "w", encoding="utf-8").write("\n".join(rows))
print(f"gallery written to {out}")
