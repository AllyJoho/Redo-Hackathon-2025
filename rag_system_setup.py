"""
RAG System Setup - Creates vector database and embeddings for BYU course advisor.
This uses 100% FREE tools: Chroma + Sentence Transformers (no API keys needed!)
"""

import json
from pathlib import Path
from typing import List, Dict
import chromadb
from sentence_transformers import SentenceTransformer

class BYUCourseRAG:
    """
    Builds a RAG (Retrieval Augmented Generation) system for course recommendations.
    Uses local embeddings and vector database - no API costs!
    """
    
    def __init__(self, data_dir: str = "data", db_dir: str = "chroma_db"):
        """
        Initialize the RAG system.
        
        Args:
            data_dir: Directory containing JSON files
            db_dir: Directory to store Chroma database
        """
        self.data_dir = Path(data_dir)
        self.db_dir = Path(db_dir)
        self.db_dir.mkdir(exist_ok=True)
        
        print("🔧 Initializing RAG system...")
        print("   • Loading embedding model (this may take a moment)...")
        
        # Load the embedding model (runs locally, no API needed!)
        # Using a small, fast model perfect for hackathons
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        print("   ✓ Embedding model loaded!")
        
        # Initialize Chroma DB
        self.client = chromadb.PersistentClient(path=str(self.db_dir))
        
        # Load data
        self.programs = self._load_json("programs.json")
        self.classes = self._load_json("classes.json")
        self.class_overlap = self._load_json("class_overlap.json")
        
        print(f"   ✓ Loaded {len(self.programs)} programs")
        print(f"   ✓ Loaded {len(self.classes)} classes")
    
    def _load_json(self, filename: str) -> List[Dict]:
        """Load JSON data file."""
        filepath = self.data_dir / filename
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def build_vector_database(self):
        """
        Build the vector database with all course and program information.
        This is the core of the RAG system!
        """
        print("\n" + "=" * 70)
        print("🔨 BUILDING VECTOR DATABASE")
        print("=" * 70)
        
        # Create collections for different types of data
        collections = {
            "programs": self._create_program_collection(),
            "classes": self._create_class_collection(),
            "overlap": self._create_overlap_collection()
        }
        
        print("\n✓ Vector database built successfully!")
        print(f"   Database location: {self.db_dir}")
        return collections
    
    def _create_program_collection(self):
        """Create collection for program information."""
        print("\n📚 Creating program collection...")
        
        # Delete existing collection if it exists
        try:
            self.client.delete_collection("programs")
        except Exception:
            pass
        
        collection = self.client.create_collection(
            name="programs",
            metadata={"description": "BYU major programs and requirements"}
        )
        
        # Prepare documents for embedding
        documents = []
        metadatas = []
        ids = []
        
        for prog in self.programs:
            # Create rich text description for embedding
            doc_text = f"""
            Program: {prog['program_name']}
            Category: {prog['program_category']}
            Credit Hours: {prog['min_credit_hours']}-{prog['max_credit_hours']}
            
            Required Classes:
            {', '.join(prog['required_classes'])}
            
            Key Electives:
            {', '.join(prog.get('key_electives', []))}
            
            This program is ideal for students interested in {prog['program_category'].lower()}.
            """
            
            documents.append(doc_text.strip())
            metadatas.append({
                "program_id": prog["program_id"],
                "program_name": prog["program_name"],
                "category": prog["program_category"],
                "type": "program"
            })
            ids.append(f"prog_{prog['program_id']}")
        
        # Add to collection
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"   ✓ Added {len(documents)} programs to database")
        return collection
    
    def _create_class_collection(self):
        """Create collection for class information."""
        print("\n📖 Creating class collection...")
        
        try:
            self.client.delete_collection("classes")
        except Exception:
            pass
        
        collection = self.client.create_collection(
            name="classes",
            metadata={"description": "BYU course information"}
        )
        
        documents = []
        metadatas = []
        ids = []
        
        for cls in self.classes:
            # Create detailed description
            prereq_text = f"Prerequisites: {cls['prerequisites']}" if cls['prerequisites'] else "No prerequisites"
            programs_text = f"Applies to: {', '.join(cls['applies_to_programs'])}"
            
            doc_text = f"""
            Course: {cls['course_name']} - {cls['title']}
            Credits: {cls['credit_hours']}
            Category: {cls['category']}
            
            Description:
            {cls['description']}
            
            {prereq_text}
            
            {programs_text}
            
            This course is essential for students in {cls['category']}.
            """
            
            documents.append(doc_text.strip())
            metadatas.append({
                "course_id": cls["course_id"],
                "course_name": cls["course_name"],
                "title": cls["title"],
                "credit_hours": cls["credit_hours"],
                "category": cls["category"],
                "program_count": len(cls["applies_to_programs"]),
                "type": "class"
            })
            ids.append(f"class_{cls['course_id']}")
        
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"   ✓ Added {len(documents)} classes to database")
        return collection
    
    def _create_overlap_collection(self):
        """Create collection for multi-major classes (THE KEY TO YOUR PROJECT!)."""
        print("\n🎯 Creating overlap collection (multi-major classes)...")
        
        try:
            self.client.delete_collection("overlap")
        except Exception:
            pass
        
        collection = self.client.create_collection(
            name="overlap",
            metadata={"description": "Classes that apply to multiple majors"}
        )
        
        documents = []
        metadatas = []
        ids = []
        
        for cls in self.class_overlap:
            programs_list = ', '.join(cls['applies_to_programs'])
            
            doc_text = f"""
            VERSATILE COURSE: {cls['course_name']} - {cls['title']}
            
            This course counts toward {cls['program_count']} different majors:
            {programs_list}
            
            Description: {cls['description']}
            
            Prerequisites: {cls['prerequisites'] if cls['prerequisites'] else 'None'}
            
            Versatility Score: {cls['versatility_score']}/100
            
            RECOMMENDATION: This is an excellent choice for undecided students exploring 
            {cls['category']} fields. Taking this course keeps options open across 
            {cls['program_count']} programs.
            """
            
            documents.append(doc_text.strip())
            metadatas.append({
                "course_id": cls["course_id"],
                "course_name": cls["course_name"],
                "title": cls["title"],
                "program_count": cls["program_count"],
                "versatility_score": cls["versatility_score"],
                "category": cls["category"],
                "type": "overlap"
            })
            ids.append(f"overlap_{cls['course_id']}")
        
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"   ✓ Added {len(documents)} multi-major classes to database")
        return collection
    
    def test_search(self):
        """Test the search functionality with sample queries."""
        print("\n" + "=" * 70)
        print("🧪 TESTING SEARCH FUNCTIONALITY")
        print("=" * 70)
        
        test_queries = [
            "I'm interested in business and technology",
            "I want to learn programming and data analysis",
            "What math classes work for multiple majors?",
            "Classes for undecided students interested in STEM"
        ]
        
        # Get the collections
        programs_col = self.client.get_collection("programs")
        classes_col = self.client.get_collection("classes")
        overlap_col = self.client.get_collection("overlap")
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n{i}. Query: '{query}'")
            print("-" * 70)
            
            # Search overlap collection (most important for your use case)
            results = overlap_col.query(
                query_texts=[query],
                n_results=3
            )
            
            documents = results.get('documents')
            metadatas = results.get('metadatas')
            if (
                documents is not None and len(documents) > 0 and documents[0]
                and metadatas is not None and len(metadatas) > 0 and metadatas[0]
            ):
                print("   Top Recommendations:")
                for j, (doc, metadata) in enumerate(zip(documents[0], 
                                                        metadatas[0]), 1):
                    course_name = metadata.get('course_name', 'Unknown')
                    title = metadata.get('title', 'Unknown')
                    prog_count = metadata.get('program_count', 0)
                    print(f"   {j}. {course_name} - {title}")
                    print(f"      → Applies to {prog_count} majors")
    
    from typing import Optional

    def get_recommendations(self, student_interests: str, 
                           considering_majors: Optional[List[str]] = None,
                           n_results: int = 5) -> Dict:
        """
        Get course recommendations based on student interests.
        
        Args:
            student_interests: Description of student's interests/goals
            considering_majors: List of majors student is considering (optional)
            n_results: Number of recommendations to return
            
        Returns:
            Dictionary with recommendations and explanations
        """
        overlap_col = self.client.get_collection("overlap")
        classes_col = self.client.get_collection("classes")
        
        # Build enhanced query
        query = f"{student_interests}"
        if considering_majors:
            query += f" Considering majors: {', '.join(considering_majors)}"
        
        # Search for versatile courses
        overlap_results = overlap_col.query(
            query_texts=[query],
            n_results=n_results
        )
        
        recommendations = {
            "query": student_interests,
            "courses": [],
            "explanation": ""
        }
        
        documents = overlap_results.get('documents')
        metadatas = overlap_results.get('metadatas')
        if (
            documents is not None and len(documents) > 0 and documents[0]
            and metadatas is not None and len(metadatas) > 0 and metadatas[0]
        ):
            for doc, metadata in zip(documents[0], metadatas[0]):
                recommendations["courses"].append({
                    "course_name": metadata['course_name'],
                    "title": metadata['title'],
                    "program_count": metadata['program_count'],
                    "versatility_score": metadata['versatility_score']
                })
        
        return recommendations


def main():
    """Main setup function."""
    print("=" * 70)
    print("🎓 BYU UNDECIDED MAJOR ADVISOR - RAG SYSTEM SETUP")
    print("=" * 70)
    
    # Initialize RAG system
    rag = BYUCourseRAG()
    
    # Build vector database
    collections = rag.build_vector_database()
    
    # Test the system
    rag.test_search()
    
    print("\n" + "=" * 70)
    print("✅ RAG SYSTEM READY!")
    print("=" * 70)
    print("\n📝 NEXT STEPS:")
    print("   1. The vector database is now ready in ./chroma_db/")
    print("   2. Run the chatbot UI: python chatbot_ui.py")
    print("   3. Start recommending courses to undecided students!")
    print("\n💡 TIP: The 'overlap' collection is the key to your project!")
    print("   It contains courses that count toward multiple majors.")
    print("=" * 70)


if __name__ == "__main__":
    main()
