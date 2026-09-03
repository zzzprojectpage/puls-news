# Publish PULS News with GitHub Pages

This folder is the repository root. Upload its **contents**, including
`.nojekyll`.

1. Create a new public GitHub repository, for example `puls-news`.
2. Use **Add file → Upload files** and upload every item from this folder.
3. Commit the files to the `main` branch.
4. Open **Settings → Pages**.
5. Under **Build and deployment**, choose **Deploy from a branch**.
6. Select branch `main`, folder `/(root)`, then **Save**.
7. Open:
   `https://YOUR-GITHUB-USERNAME.github.io/puls-news/`

The files use relative paths and work from the GitHub repository subpath.
GitHub Pages supplies HTTPS, installation support, and the offline app shell.

## Important public-site limits

- New headlines require internet access in the visitor's browser.
- Publishers or public feed-conversion services may block CORS, throttle, or
  change their interfaces; PULS falls back to its short embedded snapshot.
- Public source/feed URLs may be sent to the fallback providers documented in
  `README.md`.
- The repository does not contain API keys, credentials, full article text, or
  copied publisher images.
- Article rights remain with the linked publishers.
