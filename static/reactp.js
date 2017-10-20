"use strict";

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

function Stat(props) {
  return React.createElement(
    "button",
    { className: "stat", onClick: props.onClick },
    props.value
  );
}

var Board = function (_React$Component) {
  _inherits(Board, _React$Component);

  function Board() {
    _classCallCheck(this, Board);

    return _possibleConstructorReturn(this, (Board.__proto__ || Object.getPrototypeOf(Board)).apply(this, arguments));
  }

  _createClass(Board, [{
    key: "renderStat",
    value: function renderStat(i) {
      var _this2 = this;

      return React.createElement(Stat, {
        value: this.props.stat[i],
        onClick: function onClick() {
          return _this2.props.onClick(i);
        }
      });
    }
  }, {
    key: "render",
    value: function render() {

      return React.createElement(
        "div",
        null,
        React.createElement(
          "div",
          { className: "board-row" },
          this.renderStat(0),
          this.renderStat(1),
          this.renderStat(2),
          this.renderStat(3),
          this.renderStat(4)
        )
      );
    }
  }]);

  return Board;
}(React.Component);

var Project = function (_React$Component2) {
  _inherits(Project, _React$Component2);

  function Project() {
    _classCallCheck(this, Project);

    var _this3 = _possibleConstructorReturn(this, (Project.__proto__ || Object.getPrototypeOf(Project)).call(this));

    _this3.state = {
      isDetailsVisible: Array(5).fill(true)
    };
    return _this3;
  }

  _createClass(Project, [{
    key: "handleClick",
    value: function handleClick(i) {
      var isAbout = this.state.isDetailsVisible.slice();
      isAbout[i] = this.state.isDetailsVisible[i] ? false : true;
      this.setState({
        isDetailsVisible: isAbout

      });
    }
  }, {
    key: "render",
    value: function render() {
      var _this4 = this;

      var id = this.props.value[1];
      var url = '/projects/';
      url = url.concat(id);
      return React.createElement(
        "div",
        null,
        React.createElement(
          "button",
          { onClick: function onClick(i) {
              return _this4.handleClick(i);
            } },
          React.createElement(
            "a",
            { href: url} ,
            React.createElement(
              "h3",
              { "class": "title" },
              " ",
              this.props.value[0],
              " "
            )
          )
        )
      );
    }
  }]);

  return Project;
}(React.Component);

var Detail = function (_React$Component3) {
  _inherits(Detail, _React$Component3);

  function Detail() {
    _classCallCheck(this, Detail);

    return _possibleConstructorReturn(this, (Detail.__proto__ || Object.getPrototypeOf(Detail)).apply(this, arguments));
  }

  _createClass(Detail, [{
    key: "render",
    value: function render() {
      return React.createElement(
        "h1",
        null,
        this.props.value
      );
    }
  }]);

  return Detail;
}(React.Component);

var App = function (_React$Component4) {
  _inherits(App, _React$Component4);

  function App() {
    _classCallCheck(this, App);

    var _this6 = _possibleConstructorReturn(this, (App.__proto__ || Object.getPrototypeOf(App)).call(this));

    _this6.state = {
      stat: ['Need Update', 'Updated', 'Finished', 'Hibernating', 'Frogged'],
      isProjectsVisible: false,
      projects: []
    };
    return _this6;
  }

  _createClass(App, [{
    key: "getProjects",
    value: function getProjects(i) {
      var _this7 = this;

      // Get the melons via AJAX
      //
      // We could use jQuery here for our AJAX request, but it seems
      // silly to bring in all of jQuery just for one tiny part.
      // Therefore, we use the new built-into-JS "fetch" API for
      // AJAX requests. Not all browsers support this, so we have
      // a "polyfill" for it in index.html.

      this.setState({ statusText: "Loading", statusType: "warning" });
      var currentStat = this.state.stat[i];
      var URL = 'projects-json/';
      URL = URL.concat(currentStat);
      fetch(URL).then(function (r) {
        return r.json();
      }).then(function (j) {
        return _this7.setState({
          projects: j.projects,
          statusText: "Loaded",
          statusType: "info"
        });
      });
      console.log(this.state.projects);
    }
  }, {
    key: "handleClick",
    value: function handleClick(i) {
      var isAbout = this.state.isProjectsVisible;
      isAbout = this.state.isProjectsVisible ? false : true;
      this.setState({
        isProjectsVisible: isAbout

      });
      this.getProjects(i);
    }
  }, {
    key: "render",
    value: function render() {
      var _this8 = this;

      return React.createElement(
        "div",
        { className: "app" },
        React.createElement(
          "div",
          { className: "project-types" },
          React.createElement(Board, { stat: this.state.stat, onClick: function onClick(i) {
              return _this8.handleClick(i);
            } })
        ),
        this.state.isProjectsVisible ? React.createElement(
          "div",
          { className: "projects" },
          this.state.projects.map(function (project) {
            return React.createElement(Project, { value: project });
          }),
      ) : null);
    }
  }]);

  return App;
}(React.Component);

// ========================================

ReactDOM.render(React.createElement(App, null), document.getElementById('root'));