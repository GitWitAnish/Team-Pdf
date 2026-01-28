import React, { useState, useEffect } from "react";
import { ChevronRight } from "lucide-react";
import "./CategoriesView.css";

function CategoriesView({ onServiceClick, viewMode }) {
  const [categories, setCategories] = useState({});
  const [allServices, setAllServices] = useState([]);

  useEffect(() => {
    fetch("/navigation_data.json")
      .then((res) => res.json())
      .then((data) => {
        const categorized = {};
        const services = [];

        data.services.forEach((service) => {
          if (service.category && service.service_name) {
            if (!categorized[service.category]) {
              categorized[service.category] = [];
            }
            categorized[service.category].push(service);
            services.push(service);
          }
        });

        setCategories(categorized);
        setAllServices(services);
      })
      .catch((error) => {
        console.error("Error loading categories:", error);
      });
  }, []);

  const handleServiceClick = (service) => {
    if (onServiceClick) {
      onServiceClick(service);
    }
  };

  if (viewMode === "categories") {
    return (
      <div className="categories-view">
        <div className="categories-header-section">
          <h2>All Categories</h2>
          <p className="categories-subtitle">
            Browse services organized by category
          </p>
        </div>

        <div className="categories-grid">
          {Object.entries(categories)
            .sort(([a], [b]) => a.localeCompare(b))
            .map(([category, services]) => (
              <div key={category} className="category-card">
                <div className="category-card-header">
                  <h3>{category}</h3>
                  {/* <span className="service-count">
                    {services.length} services
                  </span> */}
                </div>
                <div className="category-services-preview">
                  {services.slice(0, 3).map((service, idx) => (
                    <div
                      key={idx}
                      className="service-preview-item"
                      onClick={() => handleServiceClick(service)}
                    >
                      <ChevronRight size={16} />
                      <span>{service.service_name}</span>
                    </div>
                  ))}
                  {services.length > 3 && (
                    <span className="more-services">
                      +{services.length - 3} more
                    </span>
                  )}
                </div>
              </div>
            ))}
        </div>
      </div>
    );
  }

  // Subcategories view - shows all services in a list
  return (
    <div className="categories-view">
      <div className="categories-header-section">
        <h2>📋 All Services</h2>
        <p className="categories-subtitle">
          Complete list of all available services ({allServices.length} total)
        </p>
      </div>

      <div className="services-list-view">
        {Object.entries(categories)
          .sort(([a], [b]) => a.localeCompare(b))
          .map(([category, services]) => (
            <div key={category} className="category-section-list">
              <h3 className="category-title-list">{category}</h3>
              <div className="services-grid">
                {services.map((service, idx) => (
                  <div
                    key={idx}
                    className="service-card"
                    onClick={() => handleServiceClick(service)}
                  >
                    <div className="service-card-content">
                      <span className="service-icon">📄</span>
                      <span className="service-name">
                        {service.service_name}
                      </span>
                    </div>
                    <ChevronRight size={18} className="service-arrow" />
                  </div>
                ))}
              </div>
            </div>
          ))}
      </div>
    </div>
  );
}

export default CategoriesView;
