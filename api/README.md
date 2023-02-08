# Definitions

## Prefix

| JSON Prefix | Description | 
| - | - |
| t1_ | Comment chain | 
| t2_ | Account; author of a comment or thread | 
| t3_ | Specific comment within a thread; this is how child comments reference a parent comment/thread. <br> For example: A comment will be given id "j654l1g", comments replying to it will have tag "parent_id": "t3_j654l1g". <br> This chain begins at a lone comment in a thread whose parent_id will reference the thread itself. 
| t4_ | Personal Message | 
| t5_ | Subreddit | 
| t6_ | Award | 


## Submission Object (thread/post)

| Field | Data Type | Description | 
| - | - | - |
| author | Redditor Object | See 'Author Object' table | 
| author_fullname | string | t2_ prefix + author unique id <br> ex: 't2_137iwh'
| comments | CommentForest Object | See 'Comments Object' table | 
| created_utc | float | Epoch timestamp of when the thread was created | 
| fullname | string | t3_ prefix + link to unique reddit thread in a given subreddit <br> ex: 't3_10rs0tf' fetched from subreddit xyz can be linked to as such: <br> reddit.com/r/xyz/comments/10rs0tf/ |
| id | string | t3 id; link to thread without the 't3_' prefix <br> ex: '10r0tf' |
| link_flair_text | string | Flair given to a thread, such as "Retirement" or "Employment" | 
| num_comments | string | Number of comments within the given thread | 
| permalink | string | Suffix of a given thread <br> ex: /r/Catmemes/comments/uwo6hm/ThreadTitle |
| score | int | Score of thread (Upvotes - Downvotes ?) |
| selftext | string | Text posted by thread author |
| selftext_html | string | Text posted by thread author in HTML format |
| shortlink | string | Direct link to specific thread <br> ex: 'https://redd.it/v4ds3y'
| subreddit | Subreddit object | Several fields pertaining to the subreddit which the thread belongs to |
| subreddit_id | string | t5_ prefix + subreddit unique id <br> ex: 't5_2r9po' | 
| subreddit_name_prefixed | string | Name of subreddit with 'r/' prefix <br> ex: 'r/WallstreetBets' |
| subreddit_subscribers | int | Number of users subscribed to the specific subreddit | 
| title | string | Title of the submission |
| ups | int | Number of upvotes that the thread has | 
| upvote_ratio | float | Upvote to downvote ratio of thread | 
| url | string | URL provided by thread. Generally populated when a thread is an image/link post | 
| user_reports | list | List of reports that the thread has received |
| | |

<br><br>

## CommentForest Object (comments)

| Field | Data Type | Description | 
| - | - | - |
| author | Redditor Object | See 'Author Object' table | 
| author_fullname | string | t2_ prefix + author unique id <br> ex: 't2_137iwh' | 
| body | string | Comment content | 
| body_html | string | Comment content in HTML format |
| controversiality | int | How controversial a comment is |
| created_utc | float | Epoch timestamp of when the comment was created | 
| depth | int | Depth of the comment within a CommentForest starting from 0 index <br> If 'is_root' = True, then the depth is 0.  |
| edited | bool | True if the comment was ever edited | 
| fullname | string | t1_ prefix + link to unique reddit comment in a given thread <br> ex: 't1_j6vrh6g' |
| id | string | t1 id; link to comment without the 't1_' prefix <br> ex: 'j6vrh6g' |
| is_root | boolean | True if this is a top-level comment; not the child of another comment |
| is_submitter | boolean | True if the author of thread is also the author of the comment |
| link_id | string | t3_ prefix + link to unique reddit thread where the comment was posted |
| locked | boolean | True if the thread is locked; no comments may be posted to it | 
| permalink | string | Suffix of a given comment within a thread <br> ex: /r/GuildWars2/comments/10rf5xx/angry_avian/j6vrh6g |
| score | int | Score of specific comment | 
| submission | Submission Object | See 'Submission Object' table |
| subreddit | Subreddit Object | Several fields pertaining to the subreddit which the comment belongs to |
| subreddit_id | string | t5_ prefix + subreddit unique id <br> ex: 't5_10rf5xx' | 
| subreddit_name_prefixed | string | Name of subreddit with 'r/' prefix <br> ex: 't5_2r9po' |
| ups | int | Number of upvotes that the comment has | 
| user_reports | list | List of reports that the comment has received |
| | |

<br><br>

## Redditor Object (author)

| Field | Data Type | Description | 
| - | - | - |
| comment_karma | int | A given author's total comment karma |
| created_utc | float | Epoch timestamp of when the author account was created |
| fullname | str | t2_prefix + author unique id | 
| has_verified_email | bool | True if the user has verified their email | 
| id | string | t2 id; link to author without 't2_' prefix | 
| linked_karma | int | A given author's total post karma |
| name | string | The name of the author | 
| | |

