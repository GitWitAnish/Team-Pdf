import React from "react";
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
  GraduationCap,
  Stethoscope,
  Users,
  Gavel,
  Globe,
  Plane,
  BookOpen,
  Camera,
  Wifi,
  Smartphone,
  MapPin,
  Calendar,
  Clock,
  UserPlus,
  Key,
  Award,
  Clipboard,
  PlusCircle,
  UserX,
  FileCheck,
  Banknote,
  Receipt,
  CreditCard as CardIcon,
  Landmark,
  Calculator,
  TrendingUp,
  Users as HandshakeIcon,
  Scale,
  FileImage,
  Download,
  Upload,
  QrCode,
  Printer,
  Mail,
  PhoneCall,
} from "lucide-react";

export const categories = [
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
      {
        icon: <AlertCircle size={20} />,
        title: "Consumer Rights & Complaints",
        text: "उपभोक्ता अधिकार र गुनासो",
        query: "How can I file a consumer complaint in Nepal?",
      },
      {
        icon: <Shield size={20} />,
        title: "Public Service Grievance",
        text: "सार्वजनिक सेवा गुनासो",
        query: "How do I report poor public service in Nepal?",
      },
      {
        icon: <Gavel size={20} />,
        title: "Anti-Corruption Helpline",
        text: "भ्रष्टाचार विरोधी हेल्पलाइन",
        query: "How can I report corruption in Nepal?",
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
      {
        icon: <FileCheck size={20} />,
        title: "Death Certificate",
        text: "मृत्यु दर्ता प्रमाणपत्र",
        query:
          "What is the process for obtaining a death certificate in Nepal?",
      },
      {
        icon: <UserPlus size={20} />,
        title: "Adoption Certificate",
        text: "दत्तक प्रमाणपत्र",
        query: "How do I get an adoption certificate in Nepal?",
      },
      {
        icon: <Globe size={20} />,
        title: "Passport Application",
        text: "राहदानी आवेदन",
        query: "How do I apply for a passport in Nepal?",
      },
      {
        icon: <RefreshCw size={20} />,
        title: "Passport Renewal",
        text: "राहदानी नवीकरण",
        query: "How can I renew my passport in Nepal?",
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
      {
        icon: <Users size={20} />,
        title: "Family Relationship Certificate",
        text: "पारिवारिक सम्बन्ध प्रमाणपत्र",
        query: "How do I get a family relationship certificate in Nepal?",
      },
      {
        icon: <Calendar size={20} />,
        title: "Age Determination Certificate",
        text: "उमेर निर्धारण प्रमाणपत्र",
        query:
          "What is the process for age determination certificate in Nepal?",
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
      {
        icon: <Receipt size={20} />,
        title: "Income Tax Registration",
        text: "आयकर दर्ता",
        query: "How do I register for income tax in Nepal?",
      },
      {
        icon: <Calculator size={20} />,
        title: "VAT Registration",
        text: "मूल्य अभिवृद्धि कर दर्ता",
        query: "What is the process for VAT registration in Nepal?",
      },
      {
        icon: <Banknote size={20} />,
        title: "Loan Application Process",
        text: "ऋण आवेदन प्रक्रिया",
        query: "How can I apply for a bank loan in Nepal?",
      },
      {
        icon: <TrendingUp size={20} />,
        title: "Investment & Securities",
        text: "लगानी र धितोपत्र",
        query: "How do I invest in the stock market in Nepal?",
      },
      {
        icon: <Landmark size={20} />,
        title: "Foreign Exchange",
        text: "विदेशी मुद्रा",
        query: "What are the foreign exchange regulations in Nepal?",
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
      {
        icon: <HandshakeIcon size={20} />,
        title: "Partnership Registration",
        text: "साझेदारी दर्ता",
        query: "How do I register a partnership business in Nepal?",
      },
      {
        icon: <Building size={20} />,
        title: "Industry Registration",
        text: "उद्योग दर्ता",
        query: "What is the procedure for industry registration in Nepal?",
      },
      {
        icon: <Award size={20} />,
        title: "Trade License",
        text: "व्यापार इजाजतपत्र",
        query: "How can I obtain a trade license in Nepal?",
      },
      {
        icon: <FileText size={20} />,
        title: "Import/Export License",
        text: "आयात/निर्यात इजाजतपत्र",
        query: "What is the process for import/export license in Nepal?",
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
      {
        icon: <FileImage size={20} />,
        title: "Document Translation Services",
        text: "कागजात अनुवाद सेवा",
        query: "Where can I get documents translated officially in Nepal?",
      },
      {
        icon: <QrCode size={20} />,
        title: "Digital Document Verification",
        text: "डिजिटल कागजात प्रमाणीकरण",
        query: "How can I verify digital documents in Nepal?",
      },
      {
        icon: <Printer size={20} />,
        title: "Document Printing Services",
        text: "कागजात छपाई सेवा",
        query: "Where can I get official documents printed in Nepal?",
      },
    ],
  },
  // 12. Education & Academic Services
  {
    id: "education-academic",
    icon: <GraduationCap size={24} />,
    title: "Education & Academic Services",
    titleNepali: "शिक्षा र शैक्षिक सेवा",
    subcategories: [
      {
        icon: <GraduationCap size={20} />,
        title: "School Admission Process",
        text: "विद्यालय भर्ना प्रक्रिया",
        query: "What is the school admission process in Nepal?",
      },
      {
        icon: <BookOpen size={20} />,
        title: "College/University Admission",
        text: "कलेज/विश्वविद्यालय भर्ना",
        query: "How do I apply for college admission in Nepal?",
      },
      {
        icon: <FileText size={20} />,
        title: "Educational Certificate Verification",
        text: "शैक्षिक प्रमाणपत्र प्रमाणीकरण",
        query: "How can I verify educational certificates in Nepal?",
      },
      {
        icon: <Globe size={20} />,
        title: "Foreign Education Equivalency",
        text: "विदेशी शिक्षा समानता",
        query: "How do I get foreign education equivalency in Nepal?",
      },
      {
        icon: <Award size={20} />,
        title: "Scholarship Applications",
        text: "छात्रवृत्ति आवेदन",
        query: "What scholarships are available for students in Nepal?",
      },
    ],
  },
  // 13. Health & Medical Services
  {
    id: "health-medical",
    icon: <Stethoscope size={24} />,
    title: "Health & Medical Services",
    titleNepali: "स्वास्थ्य र चिकित्सा सेवा",
    subcategories: [
      {
        icon: <Stethoscope size={20} />,
        title: "Health Insurance Registration",
        text: "स्वास्थ्य बीमा दर्ता",
        query: "How do I register for health insurance in Nepal?",
      },
      {
        icon: <FileCheck size={20} />,
        title: "Medical Certificate",
        text: "चिकित्सा प्रमाणपत्र",
        query: "How can I obtain a medical certificate in Nepal?",
      },
      {
        icon: <Users size={20} />,
        title: "Medical License for Professionals",
        text: "चिकित्सक इजाजतपत्र",
        query: "How do medical professionals get licensed in Nepal?",
      },
      {
        icon: <Building size={20} />,
        title: "Hospital Registration",
        text: "अस्पताल दर्ता",
        query: "What is the process for hospital registration in Nepal?",
      },
      {
        icon: <Flame size={20} />,
        title: "Pharmacy Registration",
        text: "औषधि पसल दर्ता",
        query: "How do I register a pharmacy in Nepal?",
      },
    ],
  },
  // 14. Immigration & Travel Services
  {
    id: "immigration-travel",
    icon: <Plane size={24} />,
    title: "Immigration & Travel Services",
    titleNepali: "आप्रवासन र यात्रा सेवा",
    subcategories: [
      {
        icon: <Plane size={20} />,
        title: "Visa Application Process",
        text: "भिसा आवेदन प्रक्रिया",
        query: "How do I apply for a visa from Nepal?",
      },
      {
        icon: <Globe size={20} />,
        title: "Work Permit Application",
        text: "काम अनुमति आवेदन",
        query: "What is the process for work permit application in Nepal?",
      },
      {
        icon: <FileText size={20} />,
        title: "Tourist Visa Extension",
        text: "पर्यटक भिसा थप",
        query: "How can I extend my tourist visa in Nepal?",
      },
      {
        icon: <MapPin size={20} />,
        title: "Residence Permit",
        text: "बसोबास अनुमति",
        query: "How do I get a residence permit in Nepal?",
      },
      {
        icon: <Users size={20} />,
        title: "Refugee Registration",
        text: "शरणार्थी दर्ता",
        query: "What is the refugee registration process in Nepal?",
      },
    ],
  },
  // 15. Digital & Technology Services
  {
    id: "digital-technology",
    icon: <Smartphone size={24} />,
    title: "Digital & Technology Services",
    titleNepali: "डिजिटल र प्रविधि सेवा",
    subcategories: [
      {
        icon: <Wifi size={20} />,
        title: "Internet Service Registration",
        text: "इन्टरनेट सेवा दर्ता",
        query: "How do I register for internet services in Nepal?",
      },
      {
        icon: <Smartphone size={20} />,
        title: "Mobile SIM Registration",
        text: "मोबाइल सिम दर्ता",
        query: "What is the process for mobile SIM registration in Nepal?",
      },
      {
        icon: <Camera size={20} />,
        title: "Digital Identity Services",
        text: "डिजिटल पहिचान सेवा",
        query: "What digital identity services are available in Nepal?",
      },
      {
        icon: <QrCode size={20} />,
        title: "E-Governance Services",
        text: "ई-शासन सेवा",
        query: "What e-governance services are available in Nepal?",
      },
      {
        icon: <Download size={20} />,
        title: "Online Service Applications",
        text: "अनलाइन सेवा आवेदन",
        query: "Which government services can I access online in Nepal?",
      },
    ],
  },
];
