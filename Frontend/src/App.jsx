
import React, { useState, useEffect } from "react";
import { io } from "socket.io-client";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Home from './pages/Home.jsx'
import Host from './pages/Host.jsx'
import Player from './pages/Player.jsx'
import Join from './pages/Join.jsx'
import HostRoom from './pages/HostRoom.jsx'






function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/host" element={<Host />} />
        <Route path="/room" element={<Player />} />
        <Route path="/join" element={<Join />} />
        <Route path="/host_room" element={<HostRoom />} />
      </Routes>
    </Router>
  );
}

export default App;
