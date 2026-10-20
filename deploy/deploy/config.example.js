// Copy to deploy/config.js and fill in. The page reads these when a browser has no saved settings.
// url, token: the Apps Script /exec address and the APP_TOKEN printed by setupV3 (anyone who can open the site can read them here).
// preview: present = faculty preview mode: a banner, a rung menu (Worked / Faded / Independent), any scenario reachable including the
//   exam one, sessions logged under "preview:<name>" and never on the student roster, and a "Send a comment" link that opens an email
//   with the build, the problem id and the session id already filled in. Leave `preview` out for a student site.
var V3_CONFIG = {
  url: "https://script.google.com/macros/s/XXXXXXXX/exec",
  token: "PASTE_APP_TOKEN",
  preview: { label: "Preview build for faculty review. Not for students.", contact: "you@marshall.edu" }
};
