# Research data

Edit data/research.json for catalogue updates. It is the authoritative published model dataset. The columns array names the fields in each model row; keep row lengths aligned and preserve numeric IDs so existing browser shortlists remain valid. Pack prices are GBP per three bags. Null means unknown, never zero.

Evidence is keyed by model ID and stores source URLs, check dates and limitations. Manufacturer claims are not independent performance tests. Existing IDs 0-20 retain inherited audit caveats; five new charger-only candidates use IDs 21-25. Current prices are unknown for four additions; historical offers are not used in cost sorting.

Run python3 scripts/build.py, then serve _site with a local HTTP server. The builder treats root index.html as a migration template, removes its legacy inline dataset and publishes an HTML page that fetches data/research.json. Do not edit the obsolete inline list: the build ignores it. _site is generated, not committed. The existing UI, local-storage key and model IDs are retained. The published page requires HTTP hosting to fetch JSON; opening it directly with file:// is not supported.

Pages deployment builds and syntax-checks the output. A passing syntax check is not a full browser or live deployment test.
