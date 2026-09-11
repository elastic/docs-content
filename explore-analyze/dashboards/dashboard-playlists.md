---
description: Create and run a playlist that rotates through multiple Kibana dashboards on a display.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Create and run dashboard playlists [dashboard-playlists]

Use a dashboard playlist to display multiple dashboards in sequence. Playlists are useful for operations walls, monitors, and other displays that need to rotate through related dashboards without manual navigation.

## Create a playlist [create-dashboard-playlist]

1. Open **Analytics** → **Dashboards**.
2. Open the **Playlists** tab.
3. Click **Create playlist**.
4. Enter a **Name** for the playlist.
5. In **Find dashboards**, search for and select the dashboards that you want to include.
6. In **Playlist order**, use the move controls to arrange the dashboards. Dashboards play from top to bottom.
7. Enter the **Rotation duration (seconds)**. The duration must be greater than zero. The default duration is 30 seconds.
8. Click **Save**.

You can edit or delete a playlist from the **Playlists** tab. To change the dashboards or their order, click the edit button for the playlist.

## Run a playlist [run-dashboard-playlist]

1. Open the **Playlists** tab.
2. Click **Start** for the playlist that you want to run.

The first dashboard opens in fullscreen presentation mode. After the configured duration, {{kib}} opens the next dashboard automatically. When the playlist reaches the last dashboard, it starts again with the first dashboard.

Use the playback controls to:

- Pause or resume playback.
- Move to the previous or next dashboard.
- See the current dashboard position in the playlist.
- Exit the playlist and return to the playlist list.

Playback runs in the browser. Changing to another {{kib}} page exits the playlist.

## Dashboard access and availability [dashboard-playlist-access]

Playlists are saved in the current {{kib}} Space. You can only select and open dashboards that you can access directly in that Space.

If a dashboard is deleted or becomes inaccessible after it is added to a playlist, {{kib}} skips it during playback. If none of the dashboards are available, playback stops and displays an error.
