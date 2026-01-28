import React, { useState } from "react";
import { motion } from "framer-motion";
import { ArrowLeft } from "lucide-react";
import logo from "/logo.jpeg";
import { categories } from "./categoriesData.jsx";
import "./Welcome.css";

function Welcome({ onSuggestionClick, showSubcategories }) {
  const [selectedCategory, setSelectedCategory] = useState(null);

  const handleCategoryClick = (category) => {
    // If category has only one subcategory, trigger it directly
    if (category.subcategories.length === 1) {
      onSuggestionClick(category.subcategories[0].query);
    } else {
      // Show subcategories page for this category
      setSelectedCategory(category);
    }
  };

  const handleBack = () => {
    setSelectedCategory(null);
  };

  // If a category is selected, show its subcategories page
  if (selectedCategory) {
    return (
      <div className="welcome-container">
        <motion.div
          className="welcome-content"
          initial={{ opacity: 0, x: 100 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -100 }}
          transition={{ duration: 0.4, ease: "easeInOut" }}
        >
          <motion.div
            className="subcategories-view"
            initial={{ opacity: 0, x: 100 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -100 }}
            transition={{ duration: 0.4, ease: "easeInOut" }}
          >
            <motion.div
              className="subcategory-header-wrapper"
              initial={{ opacity: 0, y: -30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2, duration: 0.4 }}
            >
              <motion.button
                className="back-button"
                onClick={handleBack}
                whileHover={{ scale: 1.1, x: -5 }}
                whileTap={{ scale: 0.9 }}
                transition={{ duration: 0.2 }}
              >
                <ArrowLeft size={20} />
              </motion.button>
              <motion.div
                className="subcategory-header"
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ delay: 0.3, duration: 0.4 }}
              >
                <motion.div
                  className="subcategory-header-icon"
                  initial={{ rotate: -180, scale: 0 }}
                  animate={{ rotate: 0, scale: 1 }}
                  transition={{ delay: 0.4, type: "spring", stiffness: 200 }}
                >
                  {selectedCategory.icon}
                </motion.div>
                <div>
                  <motion.h2
                    className="subcategory-header-title"
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.5, duration: 0.3 }}
                  >
                    {selectedCategory.title}
                  </motion.h2>
                  <motion.p
                    className="subcategory-header-nepali"
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.6, duration: 0.3 }}
                  >
                    {selectedCategory.titleNepali}
                  </motion.p>
                </div>
              </motion.div>
            </motion.div>
            <motion.div
              className="suggestions-grid"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.5, duration: 0.4 }}
            >
              {selectedCategory.subcategories.map((subcategory, index) => (
                <motion.button
                  key={index}
                  className="suggestion-card"
                  onClick={() => onSuggestionClick(subcategory.query)}
                  initial={{ opacity: 0, y: 30 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{
                    delay: 0.6 + index * 0.1,
                    duration: 0.4,
                    type: "spring",
                    stiffness: 100,
                  }}
                  whileHover={{
                    scale: 1.03,
                    y: -5,
                    transition: { duration: 0.2 },
                  }}
                  whileTap={{ scale: 0.97 }}
                >
                  <div className="suggestion-content">
                    <span className="suggestion-title">
                      {subcategory.title}
                    </span>
                    <span className="suggestion-text">{subcategory.text}</span>
                  </div>
                  <motion.span
                    className="suggestion-icon"
                    whileHover={{ rotate: 15, scale: 1.2 }}
                    transition={{ duration: 0.2 }}
                  >
                    {subcategory.icon}
                  </motion.span>
                </motion.button>
              ))}
            </motion.div>
          </motion.div>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="welcome-container">
      <motion.div
        className="welcome-content"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <motion.div
          className="welcome-logo-wrapper"
          initial={{ scale: 0, rotate: -180 }}
          animate={{ scale: 1, rotate: 0 }}
          transition={{
            duration: 0.6,
            type: "spring",
            stiffness: 200,
            damping: 15,
          }}
        >
          <img src={logo} alt="VIDHI.AI" className="welcome-logo" />
        </motion.div>

        <motion.h1
          className="welcome-title"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3, duration: 0.5 }}
        >
          VIDHI.AI
        </motion.h1>
        <motion.p
          className="welcome-subtitle"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4, duration: 0.5 }}
        >
          Your Legal Assistant for Nepalese Laws and Government Services
        </motion.p>

        <motion.div
          className="categories-grid"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5, duration: 0.5 }}
        >
          {categories.map((category, index) => (
            <motion.div
              key={category.id}
              className="category-card-wrapper"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{
                delay: 0.6 + index * 0.05,
                duration: 0.4,
                type: "spring",
                stiffness: 100,
              }}
            >
              <motion.button
                className="category-card"
                onClick={() => handleCategoryClick(category)}
                whileHover={{
                  scale: 1.05,
                  transition: { duration: 0.2 },
                }}
                whileTap={{ scale: 0.95 }}
              >
                <motion.div
                  className="category-icon"
                  whileHover={{ rotate: [0, -10, 10, 0] }}
                  transition={{ duration: 0.5 }}
                >
                  {category.icon}
                </motion.div>
                <div className="category-content">
                  <span className="category-title">{category.title}</span>
                  <span className="category-title-nepali">
                    {category.titleNepali}
                  </span>
                </div>
              </motion.button>

              {showSubcategories && (
                <motion.div
                  className="subcategories-list"
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: "auto" }}
                  transition={{ duration: 0.3, delay: 0.1 + index * 0.05 }}
                >
                  {category.subcategories.map((subcategory, subIndex) => (
                    <motion.button
                      key={subIndex}
                      className="subcategory-item"
                      onClick={() => onSuggestionClick(subcategory.query)}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 0.2 + subIndex * 0.05 }}
                      whileHover={{ x: 5, scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                    >
                      <span className="subcategory-icon">
                        {subcategory.icon}
                      </span>
                      <div className="subcategory-text">
                        <span className="subcategory-title">
                          {subcategory.title}
                        </span>
                        <span className="subcategory-nepali">
                          {subcategory.text}
                        </span>
                      </div>
                    </motion.button>
                  ))}
                </motion.div>
              )}
            </motion.div>
          ))}
        </motion.div>
      </motion.div>
    </div>
  );
}

export default Welcome;
