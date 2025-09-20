"""
Sentient ROMA Health Analysis Engine

Implements the recursive hierarchical structure as described in the Sentient AGI ROMA framework:
- Atomizer: Determines if tasks are atomic or need decomposition
- Planner: Breaks complex tasks into subtasks  
- Executors: Handle atomic tasks (specialized health agents)
- Aggregator: Combines subtask results into coherent final output

ROMA Process Flow:
def solve(task):
    if is_atomic(task):          # Step 1: Atomizer
        return execute(task)      # Step 2: Executor  
    else:
        subtasks = plan(task)     # Step 2: Planner
        results = []
        for subtask in subtasks:
            results.append(solve(subtask))  # Recursive call
        return aggregate(results) # Step 3: Aggregator
"""

from typing import Any, Dict, List, Optional
import asyncio
import time
from roma_agents.sentient_health_agents import (
    HealthAtomizer,
    HealthPlanner, 
    DataIngestionAgent,
    MetricsAnalysisAgent,
    CoachingAgent,
    ReportingAgent,
    HealthAggregator
)


class SentientRomaHealthRunner:
    """
    Sentient ROMA Health Analysis Engine
    
    Implements recursive hierarchical task decomposition for health analysis:
    - Top-down: Tasks decomposed into subtasks recursively
    - Bottom-up: Subtask results aggregated upwards  
    - Left-to-right: Dependencies handled sequentially
    """
    
    def __init__(self):
        print("🤖 Initializing Sentient ROMA Health Analysis Engine...")
        
        # ROMA Core Components
        self.atomizer = HealthAtomizer()
        self.planner = HealthPlanner()
        self.aggregator = HealthAggregator()
        
        # Specialized Health Executors
        self.executors = {
            "DataIngestionAgent": DataIngestionAgent(),
            "MetricsAnalysisAgent": MetricsAnalysisAgent(), 
            "CoachingAgent": CoachingAgent(),
            "ReportingAgent": ReportingAgent()
        }
        
        print("✅ ROMA agents initialized successfully")
    
    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main ROMA execution entry point
        
        Implements the recursive solve() function:
        def solve(task):
            if is_atomic(task): return execute(task)
            else:
                subtasks = plan(task)
                results = [solve(subtask) for subtask in subtasks]
                return aggregate(results)
        """
        print("🚀 Starting Sentient ROMA health analysis...")
        start_time = time.time()
        
        # Create initial task node
        initial_task = {
            "description": "Comprehensive health analysis with personalized insights and recommendations",
            "user_profile": payload.get("user_profile", {}),
            "daily_logs": payload.get("daily_logs", []),
            "targets": payload.get("targets", {}),
            "request_type": "health_analysis"
        }
        
        try:
            # Execute ROMA recursive solve function
            result = self._solve(initial_task)
            
            execution_time = time.time() - start_time
            print(f"✅ ROMA analysis completed in {execution_time:.2f}s")
            
            # Add execution metadata
            result["execution_metadata"] = {
                "framework": "Sentient ROMA v0.1",
                "execution_time_seconds": round(execution_time, 2),
                "architecture": "recursive_hierarchical_multi_agent",
                "agent_count": len(self.executors) + 3  # executors + atomizer + planner + aggregator
            }
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            print(f"❌ ROMA analysis failed after {execution_time:.2f}s: {str(e)}")
            
            return {
                "status": "error",
                "error": f"ROMA execution failed: {str(e)}",
                "roma_execution": "failed",
                "execution_time_seconds": round(execution_time, 2),
                "fallback_message": "Please check your data format and try again"
            }
    
    def _solve(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Core ROMA recursive solve function
        
        Step 1: Atomizer - Determine if task is atomic
        Step 2a: If atomic -> Execute directly  
        Step 2b: If complex -> Plan into subtasks, then recursively solve each
        Step 3: Aggregate results into final output
        """
        print(f"🔍 ROMA Solve: {task.get('description', 'Unknown task')[:50]}...")
        
        # Step 1: Atomizer - Check if task is atomic
        print("📋 Step 1: Atomizer analyzing task complexity...")
        atomization_result = self.atomizer.execute(task)
        
        if atomization_result.get("is_atomic", False):
            # Step 2a: Direct execution for atomic tasks
            suggested_agent = atomization_result.get("suggested_agent", "DataIngestionAgent")
            print(f"⚡ Task is atomic, executing with {suggested_agent}")
            
            if suggested_agent in self.executors:
                return self.executors[suggested_agent].execute(task)
            else:
                # Fallback to data ingestion for unknown agents
                return self.executors["DataIngestionAgent"].execute(task)
        
        else:
            # Step 2b: Complex task needs planning and recursive decomposition
            print("🗺️  Task is complex, initiating planning phase...")
            
            # Plan the task into subtasks
            planning_result = self.planner.execute(task)
            subtasks = planning_result.get("subtasks", [])
            
            if not subtasks:
                # Fallback to default health analysis workflow
                print("⚠️  No subtasks generated, using default workflow")
                return self._execute_default_workflow(task)
            
            print(f"📝 Generated {len(subtasks)} subtasks for execution")
            
            # Execute subtasks with dependency management
            subtask_results = self._execute_subtasks_with_dependencies(subtasks, task)
            
            # Step 3: Aggregate results
            print("🔄 Step 3: Aggregating subtask results...")
            final_result = self.aggregator.execute(subtask_results, task)
            
            return final_result
    
    def _execute_subtasks_with_dependencies(self, subtasks: List[Dict], original_task: Dict) -> Dict[str, Any]:
        """
        Execute subtasks respecting dependencies
        
        ROMA dependency handling:
        - Top-down: Task decomposition
        - Left-to-right: Dependencies respected sequentially  
        - Bottom-up: Results aggregated upwards
        """
        print("🔗 Managing subtask dependencies...")
        
        # Sort subtasks by priority and dependencies
        execution_order = self._resolve_execution_order(subtasks)
        results = {}
        
        for subtask in execution_order:
            subtask_id = subtask.get("id", f"task_{len(results)}")
            agent_name = subtask.get("agent", "DataIngestionAgent")
            
            print(f"🔄 Executing subtask: {subtask_id} with {agent_name}")
            
            # Prepare data for this subtask, including results from dependencies
            task_data = self._prepare_subtask_data(subtask, original_task, results)
            
            # Execute the subtask
            if agent_name in self.executors:
                subtask_result = self.executors[agent_name].execute(task_data)
                results[subtask_id] = subtask_result
                
                status = subtask_result.get("status", "unknown")
                print(f"✅ Subtask {subtask_id} completed with status: {status}")
            else:
                print(f"⚠️  Unknown agent {agent_name}, skipping subtask {subtask_id}")
                results[subtask_id] = {"status": "skipped", "error": f"Unknown agent: {agent_name}"}
        
        return results
    
    def _resolve_execution_order(self, subtasks: List[Dict]) -> List[Dict]:
        """
        Resolve subtask execution order based on dependencies and priorities
        
        ROMA left-to-right execution: dependent tasks wait for prerequisites
        """
        # Simple topological sort based on dependencies
        ordered_tasks = []
        remaining_tasks = subtasks.copy()
        completed_task_ids = set()
        
        while remaining_tasks:
            progress = False
            
            for task in remaining_tasks[:]:  # Copy list to avoid modification during iteration
                dependencies = task.get("depends_on", [])
                
                # Check if all dependencies are satisfied
                if all(dep_id in completed_task_ids for dep_id in dependencies):
                    ordered_tasks.append(task)
                    completed_task_ids.add(task.get("id", ""))
                    remaining_tasks.remove(task)
                    progress = True
            
            if not progress:
                # Circular dependency or missing dependency, add remaining tasks
                print("⚠️  Dependency resolution issue, adding remaining tasks in priority order")
                remaining_tasks.sort(key=lambda x: x.get("priority", 5))
                ordered_tasks.extend(remaining_tasks)
                break
        
        return ordered_tasks
    
    def _prepare_subtask_data(self, subtask: Dict, original_task: Dict, previous_results: Dict) -> Dict[str, Any]:
        """
        Prepare data for subtask execution, including outputs from dependent tasks
        
        ROMA data flow: outputs from completed subtasks become inputs to dependent subtasks
        """
        # Start with original task data
        task_data = {
            "user_profile": original_task.get("user_profile", {}),
            "daily_logs": original_task.get("daily_logs", []),
            "targets": original_task.get("targets", {}),
            "subtask_id": subtask.get("id", ""),
            "description": subtask.get("description", "")
        }
        
        # Add outputs from dependent tasks
        dependencies = subtask.get("depends_on", [])
        for dep_id in dependencies:
            if dep_id in previous_results:
                dep_result = previous_results[dep_id]
                
                # Merge specific outputs based on dependency type
                if dep_id == "data_ingestion" and dep_result.get("status") == "ok":
                    task_data["normalized_profile"] = dep_result.get("normalized_profile", {})
                    task_data["normalized_logs"] = dep_result.get("normalized_logs", [])
                    task_data["normalized_targets"] = dep_result.get("normalized_targets", {})
                
                elif dep_id == "metrics_analysis" and dep_result.get("status") == "ok":
                    task_data["metrics"] = dep_result.get("metrics", {})
                
                elif dep_id == "coaching" and dep_result.get("status") == "ok":
                    task_data["coaching"] = dep_result.get("coaching", {})
        
        return task_data
    
    def _execute_default_workflow(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fallback execution workflow when planning fails
        
        Executes standard health analysis pipeline sequentially
        """
        print("🔄 Executing default health analysis workflow...")
        
        results = {}
        
        # Step 1: Data Ingestion
        print("📥 Step 1: Data ingestion and validation...")
        ingestion_result = self.executors["DataIngestionAgent"].execute(task)
        results["data_ingestion"] = ingestion_result
        
        if ingestion_result.get("status") != "ok":
            return ingestion_result  # Return early if data validation fails
        
        # Step 2: Metrics Analysis
        print("📊 Step 2: Health metrics analysis...")
        metrics_data = {
            "normalized_profile": ingestion_result.get("normalized_profile", {}),
            "normalized_logs": ingestion_result.get("normalized_logs", []),
            "normalized_targets": ingestion_result.get("normalized_targets", {})
        }
        metrics_result = self.executors["MetricsAnalysisAgent"].execute(metrics_data)
        results["metrics_analysis"] = metrics_result
        
        # Step 3: Coaching Recommendations
        print("🎯 Step 3: Generating coaching recommendations...")
        coaching_data = {
            **metrics_data,
            "metrics": metrics_result.get("metrics", {})
        }
        coaching_result = self.executors["CoachingAgent"].execute(coaching_data)
        results["coaching"] = coaching_result
        
        # Step 4: Report Generation
        print("📋 Step 4: Generating comprehensive report...")
        report_data = {
            "normalized_profile": ingestion_result.get("normalized_profile", {}),
            "metrics": metrics_result.get("metrics", {}),
            "coaching": coaching_result.get("coaching", {})
        }
        report_result = self.executors["ReportingAgent"].execute(report_data)
        results["reporting"] = report_result
        
        # Step 5: Aggregate results  
        print("🔄 Step 5: Aggregating final results...")
        final_result = self.aggregator.execute(results, task)
        
        return final_result
    
    async def run_async(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Asynchronous version of the ROMA runner for concurrent subtask execution
        
        Future enhancement: Enable parallel execution of independent subtasks
        """
        # For now, delegate to synchronous version
        # Future: Implement true async execution with parallel subtasks
        return self.run(payload)
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get information about the ROMA system configuration"""
        return {
            "framework": "Sentient ROMA v0.1 (Beta)",
            "architecture": "Recursive Open Meta-Agent",
            "description": "Hierarchical multi-agent system for complex health analysis",
            "components": {
                "atomizer": "HealthAtomizer - Task complexity analysis",
                "planner": "HealthPlanner - Task decomposition", 
                "executors": {
                    name: f"{name} - {agent.__class__.__doc__ or 'Specialized health agent'}"
                    for name, agent in self.executors.items()
                },
                "aggregator": "HealthAggregator - Results integration"
            },
            "workflow": [
                "1. Atomizer: Analyze task complexity",
                "2a. If atomic: Execute directly with specialized agent", 
                "2b. If complex: Plan subtasks and execute recursively",
                "3. Aggregator: Integrate results into coherent output"
            ],
            "execution_patterns": [
                "Top-down: Tasks decomposed recursively",
                "Left-to-right: Dependencies respected sequentially", 
                "Bottom-up: Results aggregated upwards"
            ]
        }
