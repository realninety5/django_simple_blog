An image bookmarking/sharing site, courtesy Django by Example 3

This site allows the user to visit any site and bookmark the images there which get downloaded to their own profile
Users are also allowed to follow other users, like their images

Registratiion can be done by filling a form, or via any of these
1. Facebook Login
2. Google Login
3. Twitter Login

There is also an activity stream that displays what the users yiu are following have done recently

More so, a most viewed images functionality which displays the most viewed images.

The app uses Sqlite for models storage, but Redis for data that changes often like views rather than hit the DB all the time

Pages are secured with pyOpenSSL
