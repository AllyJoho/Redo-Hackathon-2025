"""
Generate structured JSON data from BYU program PDFs for the undecided major advisor.
This creates the exact data structure needed for your RAG system.
"""

import json
from pathlib import Path

def generate_byu_course_data():
    """
    Generate comprehensive course data based on the provided BYU program PDFs.
    This creates all the JSON files needed for your RAG chatbot.
    """
    
    # Define all programs from your PDFs
    programs_data = [
        {
            "program_id": "34302",
            "program_name": "Information Systems (BS)",
            "program_category": "Business",
            "min_credit_hours": 64,
            "max_credit_hours": 64,
            "required_classes": [
                "ACC200", "IS201", "CS111", "CS142", "IS303",  # Prerequisites (choose)
                "ECON110", "FIN201", "IS110", "MCOM320", "MKTG201", "STAT121",  # Pre-core
                "IS401", "IS402", "IS403", "IS404", "IS413", "IS414", "IS415", "IS455",  # Core
                "GSCM201", "GSCM211", "HRM391", "MSB390", "STRAT392"  # Business core
            ],
            "key_electives": [
                "IS515", "IS520", "IS531", "IS533", "IS537", "IS542", "IS543",
                "IS551", "IS555", "IS560", "IS562", "IS565", "IS566", "IS571", "IS572"
            ]
        },
        {
            "program_id": "34565",
            "program_name": "Finance (BS)",
            "program_category": "Business",
            "min_credit_hours": 64,
            "max_credit_hours": 64,
            "required_classes": [
                "ACC200", "FIN201", "ACC310",  # Prerequisites
                "ECON110", "IS110", "STAT121",  # Required early
                "FIN326", "FIN400", "FIN401", "FIN410", "FIN453",  # Core
                "ACC241", "GSCM201", "GSCM211", "IS201", "MCOM320", "MKTG201",  # Foundation
                "HRM391", "MSB390", "STRAT392"  # Business core
            ],
            "key_electives": [
                "FIN409", "FIN411", "FIN413", "FIN414", "FIN415R", "FIN418",
                "FIN420", "FIN424", "FIN425", "FIN428", "FIN432", "FIN436",
                "FIN440", "FIN444", "FIN446", "FIN451", "FIN510"
            ]
        },
        {
            "program_id": "34574",
            "program_name": "Accounting (BS)",
            "program_category": "Business",
            "min_credit_hours": 64,
            "max_credit_hours": 64,
            "required_classes": [
                "ACC200", "ACC310", "IS201",  # Prerequisites
                "ACC241", "ECON110", "FIN201", "IS110", "MCOM320", "MKTG201",  # Foundation
                "ACC401", "ACC402", "ACC403", "ACC404", "ACC405", "ACC406",  # Junior core
                "ACC407", "ACC408", "ACC409", "ACC410", "ACC411",  # Junior core cont.
                "FIN402", "HRM391", "MSB571", "STRAT392"  # Business core
            ],
            "key_electives": []
        },
        {
            "program_id": "34712",
            "program_name": "Computer Science (BS)",
            "program_category": "STEM - Computing",
            "min_credit_hours": 74,
            "max_credit_hours": 75,
            "required_classes": [
                "CS111", "CS191", "CS224", "CS235", "CS236", "CS240",  # Core 1
                "CS252", "CS260", "CS291", "CS312", "CS324", "CS340", "CS404",  # Core 2
                "MATH112", "MATH213", "MATH215", "PHSCS121", "WRTG316",  # Math/Science
                "STAT121", "STAT201", "MATH431"  # Stats (choose one)
            ],
            "key_electives": [
                "CS329", "CS330", "CS345", "CS355", "CS356", "CS428", "CS431",
                "CS450", "CS452", "CS455", "CS460", "CS465", "CS470", "CS472",
                "CS473", "CS474", "CS480", "CS481"
            ]
        },
        {
            "program_id": "34200",
            "program_name": "Computer Engineering (BS)",
            "program_category": "STEM - Engineering",
            "min_credit_hours": 90,
            "max_credit_hours": 90,
            "required_classes": [
                "CS111", "CS235", "CS236", "CS240",  # CS courses
                "ECEN191", "ECEN192", "ECEN224", "ECEN225", "ECEN240",  # ECEn core 1
                "ECEN320", "ECEN330", "ECEN340", "ECEN380", "ECEN390", "ECEN391",  # ECEn core 2
                "ECEN475", "ECEN476",  # Capstone
                "MATH112", "MATH113", "MATH213", "MATH215", "MATH334",  # Math
                "PHSCS121", "PHSCS220", "STAT201",  # Physics/Stats
                "CHEM105", "CHEM111"  # Chemistry (choose one)
            ],
            "key_electives": [
                "ECEN423", "ECEN425", "ECEN426", "ECEN427", "ECEN433",
                "CS312", "CS340", "CS345", "CS428", "CS465", "CS470", "CS472"
            ]
        },
        {
            "program_id": "34678",
            "program_name": "Mathematics (BS)",
            "program_category": "STEM - Math",
            "min_credit_hours": 53.5,
            "max_credit_hours": 53.5,
            "required_classes": [
                "CS111",  # Programming
                "MATH112", "MATH113", "MATH191", "MATH213", "MATH215",  # Calculus/Linear
                "MATH290", "MATH314", "MATH334",  # Core math
                "MATH341", "MATH342", "MATH352", "MATH371", "MATH413",  # Advanced core
                "STAT201", "MATH431"  # Stats (choose one)
            ],
            "key_electives": [
                "CS235", "MATH350", "MATH372", "MATH380", "MATH402", "MATH410",
                "MATH425", "MATH431", "MATH435", "MATH447", "MATH451", "MATH485", "MATH487"
            ]
        },
        {
            "program_id": "34703",
            "program_name": "Mathematics (BS) - Applied & Computational",
            "program_category": "STEM - Math",
            "min_credit_hours": 71,
            "max_credit_hours": 76,
            "required_classes": [
                "CS111",  # Programming
                "MATH112", "MATH113", "MATH213", "MATH215",  # Calculus/Linear
                "MATH290", "MATH314", "MATH334", "MATH341",  # Core
                "MATH320", "MATH321", "MATH344", "MATH345",  # Junior year fall
                "MATH322", "MATH323", "MATH346", "MATH347",  # Junior year winter
                "MATH402", "MATH403", "MATH436", "MATH437",  # Senior year fall
                "MATH404", "MATH405", "MATH438", "MATH439"  # Senior year winter
            ],
            "key_electives": []
        },
        {
            "program_id": "34706",
            "program_name": "Statistics (BS) - Applied Statistics & Analytics",
            "program_category": "STEM - Math/Data",
            "min_credit_hours": 53.5,
            "max_credit_hours": 53.5,
            "required_classes": [
                "STAT121", "STAT130",  # Intro
                "STAT230", "STAT240", "STAT250", "STAT330", "STAT340", "STAT390",  # Core
                "MATH112", "MATH113", "MATH213", "MATH215",  # Math foundation
                "CS110", "CS111"  # Programming (choose one)
            ],
            "key_electives": [
                "STAT435", "STAT437", "STAT451", "STAT466", "STAT469",
                "STAT482", "STAT483", "STAT486", "STAT487", "STAT531", "STAT538"
            ]
        },
        {
            "program_id": "34702",
            "program_name": "Applied Physics (BS)",
            "program_category": "STEM - Physical Science",
            "min_credit_hours": 62,
            "max_credit_hours": 64,
            "required_classes": [
                "CS111",  # Programming
                "MATH113", "MATH302", "MATH303",  # Math (or alternate track)
                "PHSCS121", "PHSCS123", "PHSCS191", "PHSCS220", "PHSCS222",  # Physics core 1
                "PHSCS225", "PHSCS230", "PHSCS240", "PHSCS245", "PHSCS291",  # Physics core 2
                "PHSCS318", "PHSCS321", "PHSCS330", "PHSCS430", "PHSCS441"  # Advanced physics
            ],
            "key_electives": [
                "ECEN466", "PHSCS442", "PHSCS471"  # Advanced (choose one)
            ]
        }
    ]
    
    # Define detailed class information
    classes_data = [
        # Business Core Classes (overlap across IS, Finance, Accounting)
        {
            "course_id": "ACC200",
            "course_name": "ACC 200",
            "title": "Principles of Accounting",
            "credit_hours": 3.0,
            "description": "Introduction to financial and managerial accounting concepts. Covers the accounting cycle, financial statements, and basic accounting principles for business decision-making.",
            "prerequisites": "",
            "category": "Business Foundation",
            "applies_to_programs": ["Information Systems (BS)", "Finance (BS)", "Accounting (BS)"]
        },
        {
            "course_id": "ACC310",
            "course_name": "ACC 310",
            "title": "Principles of Accounting 2",
            "credit_hours": 3.0,
            "description": "Continuation of ACC 200. Advanced topics in financial accounting including assets, liabilities, stockholders' equity, and financial statement analysis.",
            "prerequisites": "ACC 200",
            "category": "Business Foundation",
            "applies_to_programs": ["Finance (BS)", "Accounting (BS)"]
        },
        {
            "course_id": "IS201",
            "course_name": "IS 201",
            "title": "Introduction to Information Systems",
            "credit_hours": 3.0,
            "description": "Overview of information systems in organizations. Topics include hardware, software, databases, networks, and the strategic use of technology in business.",
            "prerequisites": "",
            "category": "Business Foundation",
            "applies_to_programs": ["Information Systems (BS)", "Finance (BS)", "Accounting (BS)"]
        },
        {
            "course_id": "ECON110",
            "course_name": "ECON 110",
            "title": "Economic Principles and Problems",
            "credit_hours": 3.0,
            "description": "Introduction to microeconomics and macroeconomics. Covers supply and demand, market structures, GDP, inflation, and economic policy.",
            "prerequisites": "",
            "category": "Business Foundation",
            "applies_to_programs": ["Information Systems (BS)", "Finance (BS)", "Accounting (BS)"]
        },
        {
            "course_id": "FIN201",
            "course_name": "FIN 201",
            "title": "Principles of Finance",
            "credit_hours": 3.0,
            "description": "Introduction to corporate finance, including time value of money, capital budgeting, risk and return, and financial statement analysis.",
            "prerequisites": "ACC 200",
            "category": "Business Foundation",
            "applies_to_programs": ["Information Systems (BS)", "Finance (BS)", "Accounting (BS)"]
        },
        {
            "course_id": "MKTG201",
            "course_name": "MKTG 201",
            "title": "Marketing Management",
            "credit_hours": 3.0,
            "description": "Introduction to marketing concepts including customer behavior, market segmentation, product development, pricing, and promotion strategies.",
            "prerequisites": "",
            "category": "Business Foundation",
            "applies_to_programs": ["Information Systems (BS)", "Finance (BS)", "Accounting (BS)"]
        },
        {
            "course_id": "MCOM320",
            "course_name": "M COM 320",
            "title": "Management Communication",
            "credit_hours": 3.0,
            "description": "Development of professional communication skills including business writing, presentations, and interpersonal communication in organizational settings.",
            "prerequisites": "",
            "category": "Business Core",
            "applies_to_programs": ["Information Systems (BS)", "Finance (BS)", "Accounting (BS)"]
        },
        {
            "course_id": "HRM391",
            "course_name": "HRM 391",
            "title": "Organizational Effectiveness",
            "credit_hours": 3.0,
            "description": "Study of organizational behavior, leadership, motivation, team dynamics, and organizational culture.",
            "prerequisites": "",
            "category": "Business Core",
            "applies_to_programs": ["Information Systems (BS)", "Finance (BS)", "Accounting (BS)"]
        },
        {
            "course_id": "MSB390",
            "course_name": "MSB 390",
            "title": "Ethics for Management",
            "credit_hours": 3.0,
            "description": "Examination of ethical decision-making in business contexts. Covers ethical frameworks, corporate social responsibility, and moral reasoning.",
            "prerequisites": "",
            "category": "Business Core",
            "applies_to_programs": ["Information Systems (BS)", "Finance (BS)"]
        },
        {
            "course_id": "STRAT392",
            "course_name": "STRAT 392",
            "title": "Strategy and Economics",
            "credit_hours": 3.0,
            "description": "Strategic management and competitive analysis. Covers industry analysis, competitive advantage, and corporate strategy.",
            "prerequisites": "",
            "category": "Business Core",
            "applies_to_programs": ["Information Systems (BS)", "Finance (BS)", "Accounting (BS)"]
        },
        {
            "course_id": "IS110",
            "course_name": "IS 110",
            "title": "Spreadsheet Skills and Business Analysis",
            "credit_hours": 1.0,
            "description": "Develop proficiency in spreadsheet software for business analysis including formulas, functions, charts, and data manipulation.",
            "prerequisites": "",
            "category": "Business Skills",
            "applies_to_programs": ["Information Systems (BS)", "Finance (BS)", "Accounting (BS)"]
        },
        
        # STEM Core Classes (Math, Stats, CS overlap)
        {
            "course_id": "MATH112",
            "course_name": "MATH 112",
            "title": "Calculus 1",
            "credit_hours": 4.0,
            "description": "Limits, derivatives, applications of derivatives, introduction to integration. Foundation for all STEM majors.",
            "prerequisites": "Precalculus or placement",
            "category": "Mathematics Core",
            "applies_to_programs": ["Computer Science (BS)", "Computer Engineering (BS)", "Mathematics (BS)", "Mathematics (BS) - Applied & Computational", "Statistics (BS) - Applied Statistics & Analytics", "Applied Physics (BS)"]
        },
        {
            "course_id": "MATH113",
            "course_name": "MATH 113",
            "title": "Calculus 2",
            "credit_hours": 4.0,
            "description": "Techniques of integration, applications of integration, sequences and series, parametric equations and polar coordinates.",
            "prerequisites": "MATH 112",
            "category": "Mathematics Core",
            "applies_to_programs": ["Computer Science (BS)", "Computer Engineering (BS)", "Mathematics (BS)", "Mathematics (BS) - Applied & Computational", "Statistics (BS) - Applied Statistics & Analytics", "Applied Physics (BS)"]
        },
        {
            "course_id": "MATH213",
            "course_name": "MATH 213",
            "title": "Elementary Linear Algebra",
            "credit_hours": 2.0,
            "description": "Systems of linear equations, matrices, determinants, vector spaces, eigenvalues and eigenvectors. Essential for computer science and engineering.",
            "prerequisites": "MATH 112",
            "category": "Mathematics Core",
            "applies_to_programs": ["Computer Science (BS)", "Computer Engineering (BS)", "Mathematics (BS)", "Mathematics (BS) - Applied & Computational", "Statistics (BS) - Applied Statistics & Analytics"]
        },
        {
            "course_id": "MATH215",
            "course_name": "MATH 215",
            "title": "Computational Linear Algebra",
            "credit_hours": 1.0,
            "description": "Computational aspects of linear algebra using software. Numerical methods for solving linear systems and eigenvalue problems.",
            "prerequisites": "MATH 213 (can be concurrent)",
            "category": "Mathematics Core",
            "applies_to_programs": ["Computer Science (BS)", "Computer Engineering (BS)", "Mathematics (BS)", "Mathematics (BS) - Applied & Computational", "Statistics (BS) - Applied Statistics & Analytics"]
        },
        {
            "course_id": "CS111",
            "course_name": "CS 111",
            "title": "Introduction to Computer Science",
            "credit_hours": 3.0,
            "description": "Introduction to programming using Python. Covers variables, control structures, functions, data structures, and problem-solving techniques.",
            "prerequisites": "",
            "category": "Computer Science Core",
            "applies_to_programs": ["Computer Science (BS)", "Computer Engineering (BS)", "Mathematics (BS)", "Mathematics (BS) - Applied & Computational", "Applied Physics (BS)"]
        },
        {
            "course_id": "CS235",
            "course_name": "CS 235",
            "title": "Data Structures",
            "credit_hours": 3.0,
            "description": "Study of data structures including arrays, linked lists, stacks, queues, trees, hash tables, and graphs. Algorithm analysis and complexity.",
            "prerequisites": "CS 111",
            "category": "Computer Science Core",
            "applies_to_programs": ["Computer Science (BS)", "Computer Engineering (BS)"]
        },
        {
            "course_id": "CS236",
            "course_name": "CS 236",
            "title": "Discrete Structures",
            "credit_hours": 3.0,
            "description": "Mathematical foundations of computer science including logic, sets, relations, functions, graphs, and proof techniques.",
            "prerequisites": "CS 111",
            "category": "Computer Science Core",
            "applies_to_programs": ["Computer Science (BS)", "Computer Engineering (BS)"]
        },
        {
            "course_id": "STAT121",
            "course_name": "STAT 121",
            "title": "Introduction to Statistical Data Analysis",
            "credit_hours": 3.0,
            "description": "Introduction to statistical thinking and data analysis. Covers descriptive statistics, probability, hypothesis testing, and regression. Used across many majors.",
            "prerequisites": "",
            "category": "Statistics Core",
            "applies_to_programs": ["Information Systems (BS)", "Finance (BS)", "Statistics (BS) - Applied Statistics & Analytics", "Computer Science (BS)"]
        },
        {
            "course_id": "STAT201",
            "course_name": "STAT 201",
            "title": "Statistics for Engineers and Scientists",
            "credit_hours": 3.0,
            "description": "Statistical methods for engineering and science. Probability distributions, hypothesis testing, regression, and design of experiments.",
            "prerequisites": "MATH 112",
            "category": "Statistics Core",
            "applies_to_programs": ["Computer Engineering (BS)", "Mathematics (BS)", "Computer Science (BS)"]
        },
        {
            "course_id": "PHSCS121",
            "course_name": "PHSCS 121",
            "title": "Introduction to Newtonian Mechanics",
            "credit_hours": 3.0,
            "description": "Mechanics including kinematics, dynamics, energy, momentum, rotation, and gravitation. Calculus-based physics for STEM majors.",
            "prerequisites": "MATH 112 (concurrent enrollment allowed)",
            "category": "Physics Core",
            "applies_to_programs": ["Computer Science (BS)", "Computer Engineering (BS)", "Applied Physics (BS)"]
        },
        {
            "course_id": "PHSCS220",
            "course_name": "PHSCS 220",
            "title": "Introduction to Electricity and Magnetism",
            "credit_hours": 3.0,
            "description": "Electrostatics, electric fields, magnetic fields, electromagnetic induction, and circuits. Essential for engineering students.",
            "prerequisites": "PHSCS 121, MATH 113",
            "category": "Physics Core",
            "applies_to_programs": ["Computer Engineering (BS)", "Applied Physics (BS)"]
        },
        
        # Specialized courses showing diversity
        {
            "course_id": "IS402",
            "course_name": "IS 402",
            "title": "Database Systems",
            "credit_hours": 3.0,
            "description": "Database design, SQL, normalization, and database management systems. Hands-on experience with relational databases.",
            "prerequisites": "IS 201",
            "category": "Information Systems",
            "applies_to_programs": ["Information Systems (BS)"]
        },
        {
            "course_id": "FIN400",
            "course_name": "FIN 400",
            "title": "Analytical Methods in Finance",
            "credit_hours": 3.0,
            "description": "Quantitative methods for financial analysis including optimization, simulation, and decision analysis.",
            "prerequisites": "FIN 201, STAT 121",
            "category": "Finance",
            "applies_to_programs": ["Finance (BS)"]
        },
        {
            "course_id": "ACC402",
            "course_name": "ACC 402",
            "title": "Cost and Managerial Accounting",
            "credit_hours": 3.0,
            "description": "Cost accounting systems, budgeting, performance measurement, and decision-making for managers.",
            "prerequisites": "ACC 310",
            "category": "Accounting",
            "applies_to_programs": ["Accounting (BS)"]
        },
        {
            "course_id": "CS240",
            "course_name": "CS 240",
            "title": "Advanced Software Construction",
            "credit_hours": 4.0,
            "description": "Software development principles, object-oriented programming, testing, debugging, and version control. Extensive programming projects.",
            "prerequisites": "CS 111",
            "category": "Computer Science",
            "applies_to_programs": ["Computer Science (BS)", "Computer Engineering (BS)"]
        },
        {
            "course_id": "MATH314",
            "course_name": "MATH 314",
            "title": "Calculus of Several Variables",
            "credit_hours": 3.0,
            "description": "Multivariable calculus including partial derivatives, multiple integrals, vector calculus, and applications.",
            "prerequisites": "MATH 113",
            "category": "Mathematics",
            "applies_to_programs": ["Mathematics (BS)", "Mathematics (BS) - Applied & Computational"]
        },
        {
            "course_id": "STAT240",
            "course_name": "STAT 240",
            "title": "Probability and Inference 1",
            "credit_hours": 3.0,
            "description": "Mathematical foundations of probability theory. Random variables, distributions, expectation, and moment generating functions.",
            "prerequisites": "MATH 112, STAT 121",
            "category": "Statistics",
            "applies_to_programs": ["Statistics (BS) - Applied Statistics & Analytics"]
        }
    ]
    
    # Build class overlap data (classes used in multiple majors)
    class_overlap_data = []
    
    # Group classes by how many programs they apply to
    for cls in classes_data:
        program_count = len(cls["applies_to_programs"])
        if program_count > 1:
            class_overlap_data.append({
                "course_id": cls["course_id"],
                "course_name": cls["course_name"],
                "title": cls["title"],
                "credit_hours": cls["credit_hours"],
                "description": cls["description"],
                "prerequisites": cls["prerequisites"],
                "category": cls["category"],
                "applies_to_programs": cls["applies_to_programs"],
                "program_count": program_count,
                "versatility_score": program_count * 10  # Higher = more versatile
            })
    
    # Sort by versatility (most programs first)
    class_overlap_data.sort(key=lambda x: x["program_count"], reverse=True)
    
    # Save all data files
    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)
    
    # Save programs.json
    with open(output_dir / "programs.json", "w") as f:
        json.dump(programs_data, f, indent=2)
    
    # Save classes.json
    with open(output_dir / "classes.json", "w") as f:
        json.dump(classes_data, f, indent=2)
    
    # Save class_overlap.json
    with open(output_dir / "class_overlap.json", "w") as f:
        json.dump(class_overlap_data, f, indent=2)
    
    # Print summary
    print("=" * 70)
    print("✓ BYU COURSE DATA GENERATION COMPLETE!")
    print("=" * 70)
    print("\n📊 STATISTICS:")
    print(f"   • {len(programs_data)} programs")
    print(f"   • {len(classes_data)} unique classes")
    print(f"   • {len(class_overlap_data)} multi-major classes")
    print("\n📁 FILES CREATED:")
    print("   • data/programs.json")
    print("   • data/classes.json")
    print("   • data/class_overlap.json")
    
    print("\n🎯 TOP 5 MOST VERSATILE CLASSES:")
    for i, cls in enumerate(class_overlap_data[:5], 1):
        programs_str = ", ".join(cls["applies_to_programs"][:3])
        if len(cls["applies_to_programs"]) > 3:
            programs_str += f" + {len(cls['applies_to_programs']) - 3} more"
        print(f"   {i}. {cls['course_name']} - {cls['title']}")
        print(f"      Applies to {cls['program_count']} programs: {programs_str}")
    
    print("\n💡 PROGRAM CATEGORIES:")
    categories = {}
    for prog in programs_data:
        cat = prog["program_category"]
        categories[cat] = categories.get(cat, 0) + 1
    for cat, count in categories.items():
        print(f"   • {cat}: {count} programs")
    
    print("\n" + "=" * 70)
    print("🚀 Ready for Phase 2: RAG System Setup!")
    print("=" * 70)

if __name__ == "__main__":
    generate_byu_course_data()
