# PULS News — GitHub Pages build

This is a static, public-safe PULS deployment. It includes an embedded snapshot
containing source-attributed headlines, links, dates, and short summaries only.
Full article text and publisher images are not bundled.

Article cards open a short source-attributed preview. Both the reader toolbar
and the prominent reader action open the complete article on the original
publisher website in a new tab. This avoids unreliable iframe embedding and
does not republish full copyrighted articles.

Live refresh runs in each visitor's browser against the public publisher/RSS
interfaces and fallback services already configured in PULS. Availability,
rate limits, CORS behavior, and publisher terms remain external dependencies.
Every article links to its original publisher.

## External data destinations

Refresh requests may go directly to configured publishers such as HotNews,
G4Media, Biziday, DeFapt, and Veridica. When direct browser access fails, the
current PULS implementation can send public feed/site URLs to:

- `r.jina.ai`
- `api.rss2json.com`
- `www.toptal.com/developers/feed2json`

The optional reader link opens `smry.ai`. User-added source URLs may also be
sent to the fallback services for feed discovery. No account credentials,
tokens, uploaded files, or private local data are sent by this repository.

See `GITHUB-PAGES-SETUP.md` for publishing instructions.
