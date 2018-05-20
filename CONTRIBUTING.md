**NOTE:** You may find the `tests` and `tools` directories useful.

The data gathering stage is accomplished with Python while the the data visualization via React. The React app was initialized with [create-react-app](https://github.com/facebookincubator/create-react-app) so it may have some tooling that is overkill for such a small project. To make changes to the source, just run the following NPM command from the GUI directory:

`$ npm install`

It will read the `package.json` file and install all dependencies in the same directory.

To start the development server (featuring hot reloading!), run:

`$ npm start`

To create a production build, run:

`$ npm run build`

It will compile, minimize, and bundle everything to the *build* directory.