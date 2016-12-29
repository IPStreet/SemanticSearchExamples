# SemanticSearchExamples
Examples of how to use IP Street's semantic search to perform prior art search and patent landscape analysis.

Full documentation can be found at [docs.ipstreet.com](http://docs.ipstreet.com/docs/)

To run examples in run.py, replace "API_KEY" on line 129 with you IP Street API key.

## Relevent Patent Search
Basic Process:

1. Input a text search seed.
2. Concept search with text search seed with [/claim_only/](http://docs.ipstreet.com/docs/claim_onlyinput)
3. Enriched concept search results with [/data/patent](http://docs.ipstreet.com/docs/datapatent)
4. Surface results to user (write to .csv in this example)

## Prior Art Searching
Basic Process:

1. Input grant number
2. Get patent's claim text and priority date with [/data/patent](http://docs.ipstreet.com/docs/datapatent)
3. Concept search with patent's claim text as search seed with [/claim_only/](http://docs.ipstreet.com/docs/claim_onlyinput)
4. Enriched concept search results with [/data/patent](http://docs.ipstreet.com/docs/datapatent)
5. Surface results to user (write to .csv in this example)

