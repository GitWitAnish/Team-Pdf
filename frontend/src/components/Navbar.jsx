import React from "react";
import { PanelLeft, Share, MoreHorizontal, Layers, List } from "lucide-react";
import logo from "/logo.jpeg";
import "./Navbar.css";

function Navbar({
  sidebarOpen,
  onToggleSidebar,
  onToggleCategories,
  showingCategories,
  categoriesViewMode,
  onToggleCategoriesMode,
}) {
  return (
    <nav className="navbar">
      <div className="navbar-left">
        {!sidebarOpen && (
          <button
            className="navbar-btn"
            onClick={onToggleSidebar}
            aria-label="Open sidebar"
          >
            <PanelLeft size={20} />
          </button>
        )}
        <img src={logo} alt="VIDHI.AI" className="navbar-logo" />
        <span className="navbar-title">VIDHI.AI</span>
      </div>
      <div className="navbar-right">
        <button
          className={`navbar-btn categories-btn ${showingCategories ? "active" : ""}`}
          onClick={onToggleCategories}
          aria-label="Toggle categories view"
        >
          <Layers size={18} />
          <span className="btn-text">
            {showingCategories ? "Hide Categories" : "Show Categories"}
          </span>
        </button>
        {showingCategories && (
          <button
            className="navbar-btn toggle-mode-btn"
            onClick={onToggleCategoriesMode}
            aria-label="Toggle view mode"
          >
            {/* {categoriesViewMode === "categories" ? (
              <>
                <List size={18} />
                <span className="btn-text">Show All Services</span>
              </>
            ) : (
              <>
                <Layers size={18} />
                <span className="btn-text">Show Categories</span>
              </>
            )} */}
          </button>
        )}
        <button className="navbar-btn" aria-label="Share">
          <Share size={18} />
        </button>
      </div>
    </nav>
  );
}

export default Navbar;
