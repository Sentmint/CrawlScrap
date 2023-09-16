# Config Notes

## JSON Format

- "Subreddits" is the root
- Each nested object will have two fields:
    - Name
        - Name of the subreddit's front page to scan
    - Filter
        - Keyword
            - Array of Keywords to check for within the comment body. Will do an Any match.
        - StartTimeUTC
            - UTC format time to compare against the comment. If the comment is after the given StartTimeUTC, it will be picked up.

<br>

<b>It is not necessary to include all filter fields, or any at all. Simply do not include the Filter field if you do not want to filter on anything, as seen in the example below.

```
{
    "Subreddits": 
    [
      {
        "Name": "SubReddit Name 01",
        "Filter": 
        {
          "Keyword": ["Text", "One"],
          "StartTimeUTC": "2020-01-01T00:00:00Z"
        }
      },
      {
        "Name": "SubReddit Name 02",
        "Filter": 
        {
          "Keyword": ["Text", "Two"]
        }
      },
      {
        "Name": "SubReddit Name 03",
        "Filter": 
        {
          "StartTimeUTC": "2020-01-01T00:00:00Z"
        }
      },
      {
        "Name": "SubReddit Name 04",
      }
    ]
}

```