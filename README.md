# TimelineRender App

This app requires `Python` and `drawsvg`, `csv` packages
You can render `PNG` or `SVG` files with any timelines using `CSV` find with data

## CSV format

    [0] row number
    [1] id
    [2] desc
    [3] start
    [4] finish,
    [5] color
    [6] caption

Example:

<i>
1;Start;Team 1;0:00:00;6:00:00;blue;Write requirements<br>
2;Execute;Team 2;6:00:00;10:50:00;green;Execution<br>
3;Finish;Testers;6:00:00;9:50:00;green;Test<br>
</i>
