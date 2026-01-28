import React, { useState } from "react";
import { motion } from "framer-motion";
import {
  CreditCard,
  UserCheck,
  User,
  CheckSquare,
  Heart,
  FileX,
  Home,
  RefreshCw,
  Building,
  DollarSign,
  Car,
  AlertCircle,
  FileText,
  Briefcase,
  Building2,
  Zap,
  Droplet,
  Flame,
  Shield,
  Search,
  Image,
  Phone,
  ArrowLeft,
} from "lucide-react";
import logo from "/logo.jpeg";
import "./Welcome.css";

const categories = [
  // 1. PRIORITY: Emergency Contact - Most Important
  {
    id: "consumer-grievances",
    icon: <Phone size={24} />,
    title: "Emergency & Public Grievances",
    titleNepali: "आपतकालीन र सार्वजनिक गुनासो",
    subcategories: [
      {
        icon: <Phone size={20} />,
        title: "Emergency Contact",
        text: "आपतकालीन सम्पर्क",
        query: "What are the emergency contact numbers in Nepal?",
      },
    ],
  },
  // 2. Civil Identity - Essential for basic identity
  {
    id: "civil-identity",
    icon: <CreditCard size={24} />,
    title: "Civil Identity & Registration",
    titleNepali: "नागरिक परिचय र दर्ता",
    subcategories: [
      {
        icon: <CreditCard size={20} />,
        title: "National ID (NID)",
        text: "राष्ट्रिय परिचय पत्र",
        query: "How do I apply for a National ID card in Nepal?",
      },
      {
        icon: <UserCheck size={20} />,
        title: "NID / Citizenship Update",
        text: "नागरिकता अद्यावधिक",
        query: "How can I update my citizenship certificate in Nepal?",
      },
      {
        icon: <User size={20} />,
        title: "Birth Certificate",
        text: "जन्म दर्ता प्रमाणपत्र",
        query:
          "What is the process for obtaining a birth certificate in Nepal?",
      },
      {
        icon: <CheckSquare size={20} />,
        title: "Voter Registration / Voter ID Card",
        text: "मतदाता परिचयपत्र",
        query: "How do I register as a voter and get a voter ID card in Nepal?",
      },
    ],
  },
  // 3. Police & Legal - Safety and security matters
  {
    id: "police-court",
    icon: <Shield size={24} />,
    title: "Police, Court & Legal",
    titleNepali: "प्रहरी, अदालत र कानूनी",
    subcategories: [
      {
        icon: <AlertCircle size={20} />,
        title: "FIR / Police Complaint Registration",
        text: "उजुरी दर्ता",
        query: "How do I file an FIR or police complaint in Nepal?",
      },
      {
        icon: <FileText size={20} />,
        title: "Police Clearance Certificate",
        text: "प्रहरी चरित्र प्रमाणपत्र",
        query:
          "What is the procedure for obtaining a police clearance certificate in Nepal?",
      },
      {
        icon: <Search size={20} />,
        title: "Court Case Status Lookup",
        text: "अदालत मुद्दा स्थिति",
        query: "How can I check the status of a court case in Nepal?",
      },
    ],
  },
  // 4. Family & Civil Status - Important life events
  {
    id: "family-civil",
    icon: <Heart size={24} />,
    title: "Family & Civil Status",
    titleNepali: "पारिवारिक र नागरिक स्थिति",
    subcategories: [
      {
        icon: <Heart size={20} />,
        title: "Marriage Registration",
        text: "विवाह दर्ता",
        query: "What is the procedure for marriage registration in Nepal?",
      },
      {
        icon: <FileX size={20} />,
        title: "Divorce Registration",
        text: "सम्बन्धविच्छेद दर्ता",
        query: "How do I register a divorce in Nepal?",
      },
      {
        icon: <RefreshCw size={20} />,
        title: "Basai Sarai / Migration Certificate",
        text: "बसाई सराई प्रमाणपत्र",
        query:
          "What is the process for obtaining a migration certificate (Basai Sarai) in Nepal?",
      },
    ],
  },
  // 5. Transport & Vehicle - Daily mobility needs
  {
    id: "transport-vehicle",
    icon: <Car size={24} />,
    title: "Transport & Vehicle Services",
    titleNepali: "यातायात र सवारी साधन सेवा",
    subcategories: [
      {
        icon: <Car size={20} />,
        title: "Driving License Application",
        text: "सवारी चालक अनुमतिपत्र",
        query: "How do I apply for a driving license in Nepal?",
      },
      {
        icon: <RefreshCw size={20} />,
        title: "Driving License Renewal",
        text: "लाइसेन्स नवीकरण",
        query: "What is the process for renewing a driving license in Nepal?",
      },
      {
        icon: <FileText size={20} />,
        title: "Bluebook Recovery / Traffic Violation",
        text: "ब्लुबुक पुनःप्राप्ति",
        query:
          "How do I recover my bluebook or check traffic violations in Nepal?",
      },
      {
        icon: <AlertCircle size={20} />,
        title: "Traffic Fine Payment / E-Challan",
        text: "ट्राफिक जरिवाना भुक्तानी",
        query: "How can I pay traffic fines online in Nepal?",
      },
    ],
  },
  // 6. Land & Property - Property management
  {
    id: "land-property",
    icon: <Home size={24} />,
    title: "Land, Property & Taxation",
    titleNepali: "जग्गा, सम्पत्ति र कर",
    subcategories: [
      {
        icon: <Home size={20} />,
        title: "Land Ownership Registration Certificate",
        text: "जग्गा स्वामित्व प्रमाणपत्र",
        query:
          "How do I get a land ownership registration certificate in Nepal?",
      },
      {
        icon: <RefreshCw size={20} />,
        title: "Land Ownership Transfer",
        text: "जग्गा नामसारी",
        query: "What is the procedure for land ownership transfer in Nepal?",
      },
      {
        icon: <Building size={20} />,
        title: "Property Transfer (Land + Building)",
        text: "सम्पत्ति हस्तान्तरण",
        query: "How do I transfer property ownership in Nepal?",
      },
      {
        icon: <DollarSign size={20} />,
        title: "Property Tax Payment (Online)",
        text: "सम्पत्ति कर भुक्तानी",
        query: "How can I pay property tax online in Nepal?",
      },
    ],
  },
  // 7. Utilities - Basic public services
  {
    id: "utilities-public",
    icon: <Zap size={24} />,
    title: "Utilities & Public Services",
    titleNepali: "उपयोगिता र सार्वजनिक सेवा",
    subcategories: [
      {
        icon: <Zap size={20} />,
        title: "New Electricity Connection",
        text: "बिजुली जडान",
        query: "How do I apply for a new electricity connection in Nepal?",
      },
      {
        icon: <Zap size={20} />,
        title: "Pokhara Electricity / Power House Contact",
        text: "पोखरा बिजुली सम्पर्क",
        query:
          "What is the contact information for Pokhara electricity services?",
      },
      {
        icon: <Droplet size={20} />,
        title: "Drinking Water Connection",
        text: "खानेपानी जडान",
        query: "How do I apply for a drinking water connection in Nepal?",
      },
      {
        icon: <Flame size={20} />,
        title: "LPG Gas Connection",
        text: "ग्यास सिलिन्डर जडान",
        query:
          "What is the procedure for getting an LPG gas connection in Nepal?",
      },
    ],
  },
  // 8. Tax & Banking - Financial services
  {
    id: "tax-banking",
    icon: <DollarSign size={24} />,
    title: "Tax, Banking & Finance",
    titleNepali: "कर, बैंकिङ र वित्त",
    subcategories: [
      {
        icon: <CreditCard size={20} />,
        title: "Basic Bank Account Opening",
        text: "बैंक खाता खोल्ने",
        query: "What documents are needed to open a bank account in Nepal?",
      },
    ],
  },
  // 9. Business - Business services
  {
    id: "business-industry",
    icon: <Briefcase size={24} />,
    title: "Business & Industry Registration",
    titleNepali: "व्यवसाय र उद्योग दर्ता",
    subcategories: [
      {
        icon: <Briefcase size={20} />,
        title: "Business Registration (Sole Proprietorship)",
        text: "व्यवसाय दर्ता",
        query: "How do I register a sole proprietorship business in Nepal?",
      },
      {
        icon: <Building2 size={20} />,
        title: "Company Registration (Private Limited)",
        text: "कम्पनी दर्ता",
        query:
          "What is the process for registering a private limited company in Nepal?",
      },
    ],
  },
  // 10. Disaster Relief - Emergency welfare
  {
    id: "disaster-welfare",
    icon: <Shield size={24} />,
    title: "Disaster & Welfare Services",
    titleNepali: "विपद् र कल्याण सेवा",
    subcategories: [
      {
        icon: <Shield size={20} />,
        title: "Disaster Relief Registration",
        text: "विपद् राहत दर्ता",
        query: "How do I register for disaster relief assistance in Nepal?",
      },
    ],
  },
  // 11. Document Utilities - Support services
  {
    id: "document-utilities",
    icon: <FileText size={24} />,
    title: "Document Utilities & Digital Support",
    titleNepali: "कागजात उपयोगिता र डिजिटल समर्थन",
    subcategories: [
      {
        icon: <Search size={20} />,
        title: "Lost Document Duplicate Request",
        text: "हराएको कागजात प्रतिलिपि",
        query: "How do I request a duplicate of a lost document in Nepal?",
      },
      {
        icon: <Image size={20} />,
        title: "Photo Resizer / Compress to 300KB",
        text: "फोटो साइज घटाउने",
        query:
          "What are the photo size requirements for official documents in Nepal?",
      },
    ],
  },
];

function Welcome({ onSuggestionClick }) {
  const [selectedCategory, setSelectedCategory] = useState(null);

  const handleCategoryClick = (category) => {
    // If category has only one subcategory, trigger it directly
    if (category.subcategories.length === 1) {
      onSuggestionClick(category.subcategories[0].query);
    } else {
      setSelectedCategory(category);
    }
  };

  const handleBack = () => {
    setSelectedCategory(null);
  };

  return (
    <div className="welcome-container">
      <motion.div
        className="welcome-content"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        {!selectedCategory && (
          <>
            <motion.div
              className="welcome-logo-wrapper"
              initial={{ scale: 0, rotate: -180 }}
              animate={{ scale: 1, rotate: 0 }}
              exit={{ scale: 0, opacity: 0 }}
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
              exit={{ opacity: 0, y: -20 }}
              transition={{ delay: 0.3, duration: 0.5 }}
            >
              VIDHI.AI
            </motion.h1>
            <motion.p
              className="welcome-subtitle"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ delay: 0.4, duration: 0.5 }}
            >
              Your Legal Assistant for Nepalese Laws and Government Services
            </motion.p>
          </>
        )}

        {!selectedCategory ? (
          <motion.div
            className="categories-grid"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5, duration: 0.5 }}
          >
            {categories.map((category, index) => (
              <motion.button
                key={category.id}
                className="category-card"
                onClick={() => handleCategoryClick(category)}
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{
                  delay: 0.6 + index * 0.05,
                  duration: 0.4,
                  type: "spring",
                  stiffness: 100,
                }}
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
            ))}
          </motion.div>
        ) : (
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
        )}
      </motion.div>
    </div>
  );
}

export default Welcome;
