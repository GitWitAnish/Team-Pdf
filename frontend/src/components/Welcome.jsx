import React, { useState } from "react";
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
      <div className="welcome-content">
        <div className="welcome-logo-wrapper">
          <img src={logo} alt="Nyaya.exe" className="welcome-logo" />
        </div> 

        <h1 className="welcome-title">Nyaya.exe</h1>
        <p className="welcome-subtitle">
          Your Legal Assistant for Nepalese Laws and Government Services
        </p> 

        {!selectedCategory ? (
          <div className="categories-grid">
            {categories.map((category) => (
              <button
                key={category.id}
                className="category-card"
                onClick={() => handleCategoryClick(category)}
              >
                <div className="category-icon">{category.icon}</div>
                <div className="category-content">
                  <span className="category-title">{category.title}</span>
                  <span className="category-title-nepali">
                    {category.titleNepali}
                  </span>
                </div>
              </button>
            ))}
          </div>
        ) : (
          <div className="subcategories-view">
            <div className="subcategory-header-wrapper">
              
              <button className="back-button" onClick={handleBack}>
                <ArrowLeft size={20} />
              </button>
              <div className="subcategory-header">
                <div className="subcategory-header-icon">
                  {selectedCategory.icon}
                </div>
                <div>
                  <h2 className="subcategory-header-title">
                    {selectedCategory.title}
                  </h2>
                  <p className="subcategory-header-nepali">
                    {selectedCategory.titleNepali}
                  </p>
                </div>
              </div>
            </div>
            <div className="suggestions-grid">
              {selectedCategory.subcategories.map((subcategory, index) => (
                <button
                  key={index}
                  className="suggestion-card"
                  onClick={() => onSuggestionClick(subcategory.query)}
                >
                  <div className="suggestion-content">
                    <span className="suggestion-title">
                      {subcategory.title}
                    </span>
                    <span className="suggestion-text">{subcategory.text}</span>
                  </div>
                  <span className="suggestion-icon">{subcategory.icon}</span>
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Welcome;
