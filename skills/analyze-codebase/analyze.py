#!/usr/bin/env python3
"""
Analyze Codebase Skill Implementation

Analyzes target codebase for migration requirements and complexity.
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Any


class CodebaseAnalyzer:
    """Analyzes codebase for migration needs"""

    def __init__(self, path: str, migration_type: str, scope: str = "full"):
        self.path = Path(path).resolve()
        self.migration_type = migration_type
        self.scope = scope
        self.opencode_api = os.getenv("OPENCODE_AGENT_API", "http://localhost:8080")

    def analyze(self) -> Dict[str, Any]:
        """Run full codebase analysis"""
        print(f"🔍 Analyzing codebase at {self.path}")
        print(f"   Migration type: {self.migration_type}")
        print(f"   Scope: {self.scope}")
        print()

        result = {
            "path": str(self.path),
            "migrationType": self.migration_type,
            "scope": self.scope,
            "structure": self._analyze_structure(),
            "dependencies": self._analyze_dependencies(),
            "antiPatterns": self._detect_anti_patterns(),
            "complexity": self._calculate_complexity(),
            "migrationScore": 0,
            "recommendations": []
        }

        # Calculate overall migration score
        result["migrationScore"] = self._calculate_migration_score(result)

        # Generate recommendations
        result["recommendations"] = self._generate_recommendations(result)

        return result

    def _analyze_structure(self) -> Dict[str, Any]:
        """Analyze codebase structure"""
        print("📁 Analyzing structure...")

        structure = {
            "totalFiles": 0,
            "filesByType": {},
            "directories": [],
            "linesOfCode": 0
        }

        if not self.path.exists():
            print(f"   ⚠️  Path does not exist: {self.path}")
            return structure

        # Count files and LOC
        for ext in ['.java', '.py', '.js', '.ts', '.go', '.rb']:
            files = list(self.path.rglob(f"*{ext}"))
            if files:
                structure["filesByType"][ext] = len(files)
                structure["totalFiles"] += len(files)

                # Count LOC for this file type
                loc = 0
                for file in files:
                    try:
                        loc += len(file.read_text().splitlines())
                    except:
                        pass
                structure["linesOfCode"] += loc

        print(f"   Total files: {structure['totalFiles']}")
        print(f"   Lines of code: {structure['linesOfCode']}")

        return structure

    def _analyze_dependencies(self) -> List[Dict[str, str]]:
        """Analyze dependencies"""
        print("📦 Analyzing dependencies...")

        dependencies = []

        # Check for common dependency files
        dep_files = {
            "pom.xml": self._parse_maven_dependencies,
            "build.gradle": self._parse_gradle_dependencies,
            "package.json": self._parse_npm_dependencies,
            "requirements.txt": self._parse_python_dependencies,
            "go.mod": self._parse_go_dependencies,
        }

        for dep_file, parser in dep_files.items():
            dep_path = self.path / dep_file
            if dep_path.exists():
                print(f"   Found {dep_file}")
                dependencies.extend(parser(dep_path))

        print(f"   Total dependencies: {len(dependencies)}")
        return dependencies

    def _parse_maven_dependencies(self, path: Path) -> List[Dict[str, str]]:
        """Parse Maven dependencies from pom.xml"""
        # Simplified - in real implementation, parse XML
        return [{"name": "maven-dependencies", "version": "detected", "source": "pom.xml"}]

    def _parse_gradle_dependencies(self, path: Path) -> List[Dict[str, str]]:
        """Parse Gradle dependencies"""
        return [{"name": "gradle-dependencies", "version": "detected", "source": "build.gradle"}]

    def _parse_npm_dependencies(self, path: Path) -> List[Dict[str, str]]:
        """Parse NPM dependencies from package.json"""
        try:
            data = json.loads(path.read_text())
            deps = []
            for name, version in data.get("dependencies", {}).items():
                deps.append({"name": name, "version": version, "source": "package.json"})
            return deps
        except:
            return []

    def _parse_python_dependencies(self, path: Path) -> List[Dict[str, str]]:
        """Parse Python dependencies from requirements.txt"""
        try:
            deps = []
            for line in path.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    parts = line.split("==")
                    name = parts[0]
                    version = parts[1] if len(parts) > 1 else "latest"
                    deps.append({"name": name, "version": version, "source": "requirements.txt"})
            return deps
        except:
            return []

    def _parse_go_dependencies(self, path: Path) -> List[Dict[str, str]]:
        """Parse Go dependencies from go.mod"""
        return [{"name": "go-dependencies", "version": "detected", "source": "go.mod"}]

    def _detect_anti_patterns(self) -> List[Dict[str, Any]]:
        """Detect anti-patterns based on rule.md"""
        print("🔎 Detecting anti-patterns...")

        anti_patterns = []

        # Check for large files (God classes)
        for file in self.path.rglob("*.java"):
            try:
                lines = len(file.read_text().splitlines())
                if lines > 500:
                    anti_patterns.append({
                        "type": "GodClass",
                        "file": str(file.relative_to(self.path)),
                        "severity": "high",
                        "description": f"File has {lines} lines (threshold: 500)"
                    })
            except:
                pass

        # Check for duplicated code (simplified)
        # Real implementation would use opencode agent for this

        print(f"   Anti-patterns detected: {len(anti_patterns)}")
        return anti_patterns

    def _calculate_complexity(self) -> Dict[str, Any]:
        """Calculate complexity metrics"""
        print("📊 Calculating complexity...")

        complexity = {
            "cyclomaticComplexity": 0,
            "cognitiveComplexity": 0,
            "maintainabilityIndex": 0,
            "technicalDebt": "low"
        }

        # Simplified - real implementation uses static analysis tools
        structure = self._analyze_structure()
        loc = structure.get("linesOfCode", 0)

        # Rough estimates
        if loc < 10000:
            complexity["technicalDebt"] = "low"
            complexity["maintainabilityIndex"] = 85
        elif loc < 50000:
            complexity["technicalDebt"] = "medium"
            complexity["maintainabilityIndex"] = 65
        else:
            complexity["technicalDebt"] = "high"
            complexity["maintainabilityIndex"] = 45

        return complexity

    def _calculate_migration_score(self, analysis: Dict[str, Any]) -> int:
        """Calculate migration difficulty score (0-100, higher = easier)"""
        score = 100

        # Penalize for large codebase
        loc = analysis["structure"].get("linesOfCode", 0)
        if loc > 100000:
            score -= 30
        elif loc > 50000:
            score -= 20
        elif loc > 10000:
            score -= 10

        # Penalize for many dependencies
        dep_count = len(analysis["dependencies"])
        if dep_count > 50:
            score -= 20
        elif dep_count > 20:
            score -= 10

        # Penalize for anti-patterns
        score -= min(len(analysis["antiPatterns"]) * 5, 30)

        # Penalize for high complexity
        maintainability = analysis["complexity"].get("maintainabilityIndex", 100)
        if maintainability < 50:
            score -= 20
        elif maintainability < 70:
            score -= 10

        return max(score, 0)

    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate prioritized recommendations"""
        recommendations = []

        # Based on complexity
        if analysis["complexity"].get("technicalDebt") == "high":
            recommendations.append("Refactor high-complexity modules before migration")

        # Based on anti-patterns
        if len(analysis["antiPatterns"]) > 5:
            recommendations.append("Address anti-patterns to reduce migration risk")

        # Based on dependencies
        if len(analysis["dependencies"]) > 30:
            recommendations.append("Review and update dependencies before migration")

        # Based on migration score
        if analysis["migrationScore"] < 50:
            recommendations.append("Consider incremental migration approach")
        else:
            recommendations.append("Codebase is suitable for automated migration")

        return recommendations


def main():
    parser = argparse.ArgumentParser(description="Analyze codebase for migration")
    parser.add_argument("--path", required=True, help="Path to codebase")
    parser.add_argument("--migration-type", required=True,
                       choices=["framework", "language", "platform", "custom"],
                       help="Type of migration")
    parser.add_argument("--scope", default="full", choices=["full", "incremental"],
                       help="Analysis scope")
    parser.add_argument("--output", default="./analysis-report.json",
                       help="Output path for report")

    args = parser.parse_args()

    # Run analysis
    analyzer = CodebaseAnalyzer(args.path, args.migration_type, args.scope)
    result = analyzer.analyze()

    # Write report
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2))

    print()
    print(f"✅ Analysis complete!")
    print(f"   Report: {output_path}")
    print(f"   Migration Score: {result['migrationScore']}/100")
    print()
    print("Recommendations:")
    for rec in result["recommendations"]:
        print(f"  • {rec}")

    return 0 if result["migrationScore"] > 40 else 1


if __name__ == "__main__":
    sys.exit(main())
