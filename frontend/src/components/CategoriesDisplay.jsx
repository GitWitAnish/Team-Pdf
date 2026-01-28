import React, { useState, useEffect } from "react";
import { X, ChevronDown, ChevronRight } from "lucide-react";
import "./CategoriesDisplay.css";

function CategoriesDisplay({ isOpen, onClose, onServiceClick }) {
  const [categories, setCategories] = useState({});
  const [expandedCategories, setExpandedCategories] = useState(new Set());

  useEffect(() => {
    // Fetch navigation data and organize by categories
    fetch("/navigation_data.json")
      .then((res) => res.json())
      .then((data) => {
        const categorized = {};
        data.services.forEach((service) => {
          if (service.category && service.service_name) {
            if (!categorized[service.category]) {
              categorized[service.category] = [];
            }
            categorized[service.category].push(service);
          }
        });
        setCategories(categorized);
      })
      .catch((error) => {
        console.error("Error loading categories:", error);
      });
  }, []);

  const toggleCategory = (category) => {
    const newExpanded = new Set(expandedCategories);
    if (newExpanded.has(category)) {
      newExpanded.delete(category);
    } else {
      newExpanded.add(category);
    }
    setExpandedCategories(newExpanded);
  };

  const handleServiceClick = (service) => {
    if (onServiceClick) {
      onServiceClick(service);
    }
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="categories-overlay" onClick={onClose}>
      <div className="categories-panel" onClick={(e) => e.stopPropagation()}>
        <div className="categories-header">
          <h2>All Service Categories</h2>
          <button className="close-btn" onClick={onClose} aria-label="Close">
            <X size={24} />
          </button>
        </div>

        <div className="categories-content">
          {Object.keys(categories).length === 0 ? (
            <div className="loading">Loading categories...</div>
          ) : (
            Object.entries(categories)
              .sort(([a], [b]) => a.localeCompare(b))
              .map(([category, services]) => (
                <div key={category} className="category-section">
                  <button
                    className="category-header"
                    onClick={() => toggleCategory(category)}
                  >
                    <span className="category-icon">
                      {expandedCategories.has(category) ? (
                        <ChevronDown size={20} />
                      ) : (
                        <ChevronRight size={20} />
                      )}
                    </span>
                    <span className="category-name">{category}</span>
                    <span className="category-count">({services.length})</span>
                  </button>

                  {expandedCategories.has(category) && (
                    <div className="services-list">
                      {services.map((service, idx) => (
                        <div
                          key={idx}
                          className="service-item"
                          onClick={() => handleServiceClick(service)}
                        >
                          <span className="service-bullet">•</span>
                          <span className="service-name">
                            {service.service_name}
                          </span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))
          )}
        </div>
      </div>
    </div>
  );
}

export default CategoriesDisplay;
