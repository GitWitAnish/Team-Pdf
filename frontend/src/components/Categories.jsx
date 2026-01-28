import React from "react";
import { categories } from "./categoriesData";
import "./Categories.css";

function Categories({ onSuggestionClick }) {
  return (
    <div className="categories-container">
      <div className="categories-content">
        <div className="categories-header">
          <h1 className="categories-title">Browse Services</h1>
          <p className="categories-subtitle">
            Select a service to get started with your query
          </p>
        </div>
        <div className="categories-list">
          {categories.map((category) => (
            <div key={category.id} className="category-section">
              <div className="category-header">
                <div className="category-header-icon">{category.icon}</div>
                <div className="category-header-text">
                  <h2 className="category-header-title">{category.title}</h2>
                  <p className="category-header-nepali">
                    {category.titleNepali}
                  </p>
                </div>
              </div>
              <div className="subcategories-list">
                {category.subcategories.map((subcategory, index) => (
                  <button
                    key={index}
                    className="subcategory-card"
                    onClick={() => onSuggestionClick(subcategory.query)}
                  >
                    <div className="subcategory-icon">{subcategory.icon}</div>
                    <div className="subcategory-content">
                      <span className="subcategory-title">
                        {subcategory.title}
                      </span>
                      <span className="subcategory-text">
                        {subcategory.text}
                      </span>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Categories;
