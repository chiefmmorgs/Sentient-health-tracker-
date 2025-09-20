"""
REAL Sentient ROMA Engine - Recursive Open Meta-Agent Implementation

This implements the TRUE ROMA pattern from Sentient AGI:

def solve(task):
    if is_atomic(task):           # Atomizer decides
        return execute(task)       # Direct execution
    else:
        subtasks = plan(task)      # Planner decomposes  
        results = []
        for subtask in subtasks:
            results.append(solve(subtask))  # RECURSIVE MAGIC!
        return aggregate(results)  # Aggregator combines

This is REAL recursive hierarchical task decomposition!
"""

from typing import Any, Dict, List, Optional
import time
from roma_agents.sentient_health_agents import (
    HealthAtomizer, HealthPlanner, HealthAggregator,
    DataIngestionAgent, MetricsAnalysisAgent, 
    CoachingAgent, ReportingAgent
)

class ROMARunner:
    """
    Real Sentient ROMA Implementation
    
    Recursive Open Meta-Agent for hierarchical health analysis
    """
    
    def __init__(self):
        print("🤖 Initializing REAL Sentient ROMA Engine...")
        
        # ROMA Core Components
        self.atomizer = HealthAtomizer()
        self.planner = HealthPlanner()
        self.aggregator = HealthAggregator()
        
        # Specialized Health Executors
        self.executors = {
            "ingest": DataIngestionAgent(),
            "metrics": MetricsAnalysisAgent(),
            "coach": CoachingAgent(),
            "report": ReportingAgent(),
            # Map alternative names
            "DataIngestionAgent": DataIngestionAgent(),
            "MetricsAnalysisAgent": MetricsAnalysisAgent(),
            "CoachingAgent": CoachingAgent(),
            "ReportingAgent": ReportingAgent()
        }
        
        print("✅ REAL ROMA agents initialized successfully")
    
    def _solve(self, task: Dict[str, Any], depth: int = 0) -> Dict[str, Any]:
        """
        THE CORE ROMA RECURSIVE FUNCTION
        
        This is the real recursive solve() that implements true ROMA:
        def solve(task):
            if is_atomic(task): return execute(task)
            else:
                subtasks = plan(task)
                results = [solve(subtask) for subtask in subtasks]  # RECURSIVE!
                return aggregate(results)
        """
        indent = "  " * depth
        print(f"{indent}🔄 ROMA Solve (depth={depth}): {task.get('description', str(task)[:50])}...")
        
        # STEP 1: Atomizer - Check if task is atomic
        print(f"{indent}📋 Step 1: Atomizer analyzing task...")
        is_atomic = self.atomizer.is_atomic(task)
        
        if is_atomic:
            # STEP 2a: Direct execution for atomic tasks
            print(f"{indent}⚡ Task is ATOMIC - executing directly")
            return self._execute(task, depth)
        else:
            # STEP 2b: Complex task - decompose and recurse
            print(f"{indent}🗺️  Task is COMPLEX - planning decomposition")
            
            # Plan the task into subtasks
            subtasks = self.planner.plan(task)
            print(f"{indent}📝 Planner created {len(subtasks)} subtasks")
            
            if not subtasks:
                print(f"{indent}⚠️  No subtasks generated - executing as atomic fallback")
                return self._execute(task, depth)
            
            # STEP 3: Execute subtasks recursively with dependency management
            print(f"{indent}🔗 Executing subtasks with dependencies...")
            results = self._execute_subtasks_with_dependencies(subtasks, task, depth + 1)
            
            # STEP 4: Aggregate results
            print(f"{indent}🔄 Aggregating {len(results)} subtask results...")
            final_result = self.aggregator.combine(results, task)
            
            print(f"{indent}✅ ROMA recursion completed at depth {depth}")
            return final_result
    
    def _execute(self, task: Dict[str, Any], depth: int = 0) -> Dict[str, Any]:
        """
        Execute atomic task using appropriate specialized agent
        
        ROMA Execution: Route to the right domain expert
        """
        indent = "  " * depth
        task_kind = task.get("kind", "")
        
        # Determine which executor to use
        if task_kind in self.executors:
            executor_name = task_kind
        else:
            # Try to map task description to executor
            task_desc = task.get("description", "").lower()
            if "ingest" in task_desc or "validat" in task_desc:
                executor_name = "ingest"
            elif "metric" in task_desc or "calculat" in task_desc:
                executor_name = "metrics"
            elif "coach" in task_desc or "advice" in task_desc:
                executor_name = "coach"
            elif "report" in task_desc or "summary" in task_desc:
                executor_name = "report"
            else:
                executor_name = "ingest"  # Default fallback
        
        print(f"{indent}⚙️ Executing with {executor_name} agent...")
        
        try:
            executor = self.executors[executor_name]
            result = executor.run(task)
            
            # Ensure result has required metadata
            if isinstance(result, dict):
                result["roma_execution_depth"] = depth
                result["executor_used"] = executor_name
            
            status = result.get("ok", result.get("stage") == "ok")
            print(f"{indent}{'✅' if status else '❌'} {executor_name} completed")
            
            return result
            
        except Exception as e:
            print(f"{indent}❌ Execution failed: {str(e)}")
            return {
                "ok": False,
                "error": str(e),
                "executor_used": executor_name,
                "roma_execution_depth": depth
            }
    
    def _execute_subtasks_with_dependencies(self, subtasks: List[Dict], original_task: Dict, depth: int) -> List[Dict[str, Any]]:
        """
        Execute subtasks respecting dependencies - ROMA dependency management
        
        Left-to-right execution: dependent tasks wait for prerequisites
        """
        indent = "  " * depth
        print(f"{indent}🔗 Managing {len(subtasks)} subtasks with dependencies...")
        
        # Resolve execution order
        execution_order = self._resolve_execution_order(subtasks)
        results = []
        completed_tasks = {}
        
        for subtask in execution_order:
            subtask_id = subtask.get("id", f"task_{len(results)}")
            print(f"{indent}🔄 Executing subtask: {subtask_id}")
            
            # Prepare data for this subtask (including dependencies)
            enhanced_subtask = self._prepare_subtask_with_dependencies(
                subtask, original_task, completed_tasks, depth
            )
            
            # RECURSIVE CALL - This is where ROMA magic happens!
            subtask_result = self._solve(enhanced_subtask, depth)
            
            # Store result for dependent tasks
            completed_tasks[subtask_id] = subtask_result
            results.append(subtask_result)
            
            print(f"{indent}{'✅' if subtask_result.get('ok', True) else '❌'} Subtask {subtask_id} completed")
        
        return results
    
    def _resolve_execution_order(self, subtasks: List[Dict]) -> List[Dict]:
        """
        Topological sort for dependency-aware execution order
        
        ROMA pattern: respect dependencies while maximizing parallelization opportunities
        """
        ordered_tasks = []
        remaining_tasks = subtasks.copy()
        completed_ids = set()
        
        # Simple dependency resolution
        max_iterations = len(subtasks) * 2  # Prevent infinite loops
        iteration = 0
        
        while remaining_tasks and iteration < max_iterations:
            progress_made = False
            iteration += 1
            
            for task in remaining_tasks[:]:
                dependencies = task.get("depends_on", [])
                
                # Check if all dependencies are satisfied
                if all(dep_id in completed_ids for dep_id in dependencies):
                    ordered_tasks.append(task)
                    completed_ids.add(task.get("id", ""))
                    remaining_tasks.remove(task)
                    progress_made = True
            
            if not progress_made:
                # Circular dependency or missing dependency
                print(f"⚠️  Dependency resolution stuck, adding remaining tasks by priority")
                remaining_tasks.sort(key=lambda x: x.get("priority", 5))
                ordered_tasks.extend(remaining_tasks)
                break
        
        return ordered_tasks
    
    def _prepare_subtask_with_dependencies(self, subtask: Dict, original_task: Dict, 
                                         completed_tasks: Dict, depth: int) -> Dict[str, Any]:
        """
        Prepare subtask with data from completed dependencies
        
        ROMA data flow: outputs from completed subtasks become inputs to dependent subtasks
        """
        # Start with original task data
        enhanced_subtask = {
            "kind": subtask.get("kind", ""),
            "description": subtask.get("description", ""),
            "data": subtask.get("data", original_task.get("data", {})),
            "roma_depth": depth,
            "subtask_id": subtask.get("id", "")
        }
        
        # Add outputs from dependent tasks
        dependencies = subtask.get("depends_on", [])
        dependency_data = {}
        
        for dep_id in dependencies:
            if dep_id in completed_tasks:
                dep_result = completed_tasks[dep_id]
                
                # Merge specific outputs based on dependency type
                if "validation" in dep_id or "ingest" in dep_id:
                    if dep_result.get("normalized_data"):
                        dependency_data["normalized_data"] = dep_result["normalized_data"]
                    if dep_result.get("validation_summary"):
                        dependency_data["validation_summary"] = dep_result["validation_summary"]
                
                elif "metrics" in dep_id:
                    if dep_result.get("metrics_summary"):
                        dependency_data["metrics_summary"] = dep_result["metrics_summary"]
                    if dep_result.get("health_score"):
                        dependency_data["health_score"] = dep_result["health_score"]
                
                elif "coach" in dep_id:
                    if dep_result.get("coaching_result"):
                        dependency_data["coaching_result"] = dep_result["coaching_result"]
                
                # Always include the full result for reference
                dependency_data[f"{dep_id}_result"] = dep_result
        
        # Merge dependency data into subtask data
        if dependency_data:
            enhanced_subtask["data"].update(dependency_data)
            enhanced_subtask["dependencies_resolved"] = list(dependencies)
        
        return enhanced_subtask
    
    # Public API methods
    def run_weekly(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point for comprehensive health analysis
        
        Creates complex task that triggers ROMA recursive decomposition
        """
        print("🚀 Starting REAL ROMA weekly health analysis...")
        start_time = time.time()
        
        # Create complex task that will trigger planning
        root_task = {
            "kind": "comprehensive_health_analysis",  # Complex task type
            "description": "Comprehensive weekly health analysis with personalized insights and recommendations",
            "data": data,
            "complexity": "high",  # Hint to atomizer
            "requires": ["data_validation", "metrics_calculation", "personalized_coaching", "comprehensive_reporting"]
        }
        
        try:
            # Execute ROMA recursive solve
            result = self._solve(root_task)
            
            execution_time = time.time() - start_time
            print(f"✅ ROMA analysis completed in {execution_time:.2f}s")
            
            # Add execution metadata
            if isinstance(result, dict):
                result["roma_metadata"] = {
                    "framework": "Sentient ROMA - Recursive Open Meta-Agent",
                    "execution_time_seconds": round(execution_time, 2),
                    "pattern": "recursive_hierarchical_decomposition",
                    "version": "1.0.0"
                }
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            print(f"❌ ROMA analysis failed after {execution_time:.2f}s: {str(e)}")
            return {
                "ok": False,
                "error": f"ROMA execution failed: {str(e)}",
                "execution_time_seconds": round(execution_time, 2)
            }
    
    def analyze_single(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        """
        Quick single-entry analysis (atomic task)
        
        This should be handled as atomic by the atomizer
        """
        print("🔍 ROMA single entry analysis...")
        
        task = {
            "kind": "metrics",  # Specific atomic task
            "description": "Single entry health metrics analysis",
            "data": entry,
            "complexity": "low"  # Hint to atomizer
        }
        
        return self._solve(task)
    
    def chat(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Health coaching chat (atomic task)
        
        Simple coaching request - should be atomic
        """
        print("💬 ROMA health coaching chat...")
        
        task = {
            "kind": "coach",  # Specific atomic task  
            "description": "Health coaching conversation",
            "data": message,
            "complexity": "low"  # Hint to atomizer
        }
        
        return self._solve(task)
    
    def get_roma_info(self) -> Dict[str, Any]:
        """Get information about the ROMA system"""
        return {
            "framework": "Sentient ROMA - Recursive Open Meta-Agent",
            "version": "1.0.0",
            "description": "Hierarchical multi-agent system with true recursive task decomposition",
            "core_pattern": "solve(task) -> if atomic: execute(task) else: plan -> [solve(subtasks)] -> aggregate",
            "components": {
                "atomizer": "HealthAtomizer - AI-powered task complexity analysis",
                "planner": "HealthPlanner - Intelligent task decomposition",
                "executors": {
                    "DataIngestionAgent": "Health data validation and normalization",
                    "MetricsAnalysisAgent": "Comprehensive health metrics calculation",
                    "CoachingAgent": "Personalized health recommendations",
                    "ReportingAgent": "Comprehensive health report generation"
                },
                "aggregator": "HealthAggregator - Intelligent results synthesis"
            },
            "execution_patterns": [
                "Recursive task decomposition",
                "Dependency-aware subtask execution",
                "AI-powered planning and aggregation",
                "Hierarchical result synthesis"
            ],
            "key_features": [
                "True recursive problem solving",
                "Dynamic task planning based on complexity",
                "Specialized domain agents",
                "Intelligent result aggregation",
                "Dependency management",
                "Multi-level task hierarchy"
            ]
        }

# Backward compatibility - keep existing interface
class ROMARunner_Legacy:
    """Legacy interface for backward compatibility"""
    def __init__(self):
        self.real_runner = ROMARunner()
    
    def run_weekly(self, data):
        return self.real_runner.run_weekly(data)
    
    def analyze_single(self, entry):
        return self.real_runner.analyze_single(entry)
        
    def chat(self, message):
        return self.real_runner.chat(message)
