function Stat(props) {
  return (
    <button className="stat" onClick={props.onClick}>
      {props.value}
      
    </button>
  );
}

class Board extends React.Component {
 
  renderStat(i) {
    return (
      <Stat
        value={this.props.stat[i]}
        onClick={() => this.props.onClick(i)}
      />
    );
  }

  render() {

    return (
      <div>
        <div className="board-row">
          {this.renderStat(0)}
          {this.renderStat(1)}
          {this.renderStat(2)}
          {this.renderStat(3)}
          {this.renderStat(4)}
        </div>
      </div>
    );
  }
}
class Project extends React.Component {
  constructor() {
    super();
    this.state = {
      projects: ['hat', 'sock', 'shawl', 'sweater', 'mittens'],
      isDetailsVisible: Array(5).fill(true)
    };
  }
  getProjects: function () {
      // Get the melons via AJAX
      //
      // We could use jQuery here for our AJAX request, but it seems
      // silly to bring in all of jQuery just for one tiny part.
      // Therefore, we use the new built-into-JS "fetch" API for
      // AJAX requests. Not all browsers support this, so we have
      // a "polyfill" for it in index.html.

      this.setState({statusText: "Loading", statusType: "warning"});

      fetch("projects-json/{this.props.value}")
          .then(r => r.json())
          .then(j => this.setState({
              projects: j.melons,
              statusText: "Loaded",
              statusType: "info",
          }));
  },
  handleClick(i) {
    const isAbout = this.state.isDetailsVisible.slice();
    isAbout[i] = this.state.isDetailsVisible[i] ? false : true;
    this.setState({
      isDetailsVisible: isAbout
      
    });
  }
  render() {
    return (
      <div>
      <h3 className={this.props.value}>
        {this.props.value}
      </h3>
      <button onClick={(i) => this.handleClick(i)} ><a href="/projects/{this.state.projects[0][1]}"><h3 class='title'> { this.state.projects[0][0] } </h3></a></button>
        
       
      </div>
    );
  }
}
class Detail extends React.Component {
  render() {
    return (
      <h1>{this.props.value}</h1>
    );
  }
}
class App extends React.Component {
  constructor() {
    super();
    this.state = {
      stat: ['Need Update', 'Updated', 'Finished', 'Hibernating', 'Frogged'],
      isProjectsVisible: [false, false, false, false, false]
    };
  }
  handleClick(i) {
    const isAbout = this.state.isProjectsVisible.slice();
    isAbout[i] = this.state.isProjectsVisible[i] ? false : true;
    this.setState({
      isProjectsVisible: isAbout
      
    });
  }
  render() {
    return (
      <div className="app">
        <div className="project-types">
          <Board stat={this.state.stat} onClick={(i) => this.handleClick(i)} />
        </div>
        <div className="projects">
          { this.state.isProjectsVisible[0] ? <Project value={this.state.stat[0]}/> : null }
          { this.state.isProjectsVisible[1] ? <Project value={this.state.stat[1]}/> : null }
          { this.state.isProjectsVisible[2] ? <Project value={this.state.stat[2]}/> : null }
          { this.state.isProjectsVisible[3] ? <Project value={this.state.stat[3]}/> : null }
          { this.state.isProjectsVisible[4] ? <Project value={this.state.stat[4]}/> : null }
        </div>
      </div>
    );
  }
}

// ========================================

ReactDOM.render(
  <App />,
  document.getElementById('root')
);
