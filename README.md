Built using the Python Reddit API Wrapper [PRAW](https://praw.readthedocs.io/en/latest/index.html)

Almost all Reddit data can be made into a JSON by appending .json; optional queries can also be done to get more specific results.

| Optional | Parameter | Default | Description |
| - | - | - | - |
| ?sort= | best, top, hot, new, controversial, old, q&a | best | Will use the "sorted by" option when viewing a Reddit subreddit or thread.<br> <b>Note:</b> Any filtering will include stickied threads (pot) | 
| ?limit= | 25-100 (generally)  | 100 | Gold | 
| ?before= | t1-t5 ID | | Will get all values before this page.
| ?after= | t1-t5 ID | | Will get all values after this page.





| JSON Prefix | Description | 
| - | - |
| t1_ | Comment chain (?) | 
| t2_ | Account; author of a comment or thread | 
| t3_ | Specific comment within a thread; this is how child comments reference a parent comment/thread. <br> For example: A comment will be given id "j654l1g", comments replying to it will have tag "parent_id": "t3_j654l1g". <br> This chain begins at a lone comment in a thread whose parent_id will reference the thread itself. 
| t4_ | Message(?) | 
| t5_ | Subreddit(?) | 
| t6_ | Award | 