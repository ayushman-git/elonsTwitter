# elonsTwitter

## Environment Setup
1. Setting up env `$env:FLASK_APP = "app/run"`
2. `flask run`

## Routes
### `/posts`
**Params** - `lat=32.1231` | `long=42.1312`

**Return** - A JSON that will have `posts` and `meta` properties. `posts` will include posts within **1000km** of the given location. `meta` will contain the pagination information.

### `/post/create`
**Form Data** - `location="<lat,long>"` `text="string"`
**Return** - A JSON with message, whether the post creation was sucessful or not.

### `/weather`
**Params** - `lat=32.1231` | `long=42.1312`
**Return** - A JSON (fetched from open weather API).
