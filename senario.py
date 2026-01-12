import sys
from typing import List, Dict
import statistics

# Import from main simulation module
from main_simulation import SimulationEngine, LocationType, Region


def scenario_aggressive_investment():
    """
    Scenario 1: Aggressive Government Investment
    
    Simulates a scenario where the government heavily invests in cloud
    infrastructure from year 1, doubling investment each year.
    """
    print("\n" + "="*80)
    print("SCENARIO 1: AGGRESSIVE INVESTMENT STRATEGY")
    print("="*80)
    
    sim = SimulationEngine(num_schools=50)
    
    # Very aggressive investment schedule
    aggressive_investment = [1.5, 1.7, 1.9, 2.0, 2.0]
    
    sim.run_full_simulation(investment_schedule=aggressive_investment)
    
    # Additional analysis
    final_year = sim.metrics_history[-1]
    print(f"\n🎯 Aggressive Investment Results:")
    print(f"   Final student access: {final_year['student_access_percentage']:.2f}%")
    print(f"   Rural access achieved: {final_year['rural_access']:.2f}%")
    
    return sim


def scenario_gradual_investment():
    """
    Scenario 2: Conservative Gradual Investment
    
    Simulates a more conservative approach with gradual investment increases,
    representing budget-constrained government policy.
    """
    print("\n" + "="*80)
    print("SCENARIO 2: CONSERVATIVE GRADUAL INVESTMENT")
    print("="*80)
    
    sim = SimulationEngine(num_schools=50)
    
    # Conservative, gradual investment
    gradual_investment = [0.5, 0.6, 0.8, 1.0, 1.2]
    
    sim.run_full_simulation(investment_schedule=gradual_investment)
    
    # Compare first and last year
    first_year = sim.metrics_history[0]
    final_year = sim.metrics_history[-1]
    
    print(f"\n📊 Growth Comparison:")
    print(f"   Year 1 access: {first_year['student_access_percentage']:.2f}%")
    print(f"   Year 5 access: {final_year['student_access_percentage']:.2f}%")
    print(f"   Total growth: {final_year['student_access_percentage'] - first_year['student_access_percentage']:.2f}%")
    
    return sim


def scenario_rural_focused():
    """
    Scenario 3: Rural-Focused Initiative
    
    Analyzes what happens when we prioritize rural schools in our metrics.
    This scenario runs a normal simulation but provides detailed rural analysis.
    """
    print("\n" + "="*80)
    print("SCENARIO 3: RURAL-FOCUSED ANALYSIS")
    print("="*80)
    
    sim = SimulationEngine(num_schools=50)
    
    # Balanced investment
    balanced_investment = [0.8, 1.0, 1.2, 1.4, 1.5]
    
    sim.run_full_simulation(investment_schedule=balanced_investment)
    
    # Detailed rural analysis
    rural_schools = [s for s in sim.schools if s.location_type == LocationType.RURAL]
    
    print(f"\n🏞️  RURAL SCHOOL DETAILED ANALYSIS:")
    print(f"   Total rural schools: {len(rural_schools)}")
    print(f"   Total rural students: {sum(s.student_count for s in rural_schools):,}")
    
    # Calculate percentiles
    rural_access_scores = [s.calculate_student_access_percentage() for s in rural_schools]
    rural_access_scores.sort()
    
    print(f"\n   Access Distribution (Percentiles):")
    print(f"   • 25th percentile: {rural_access_scores[len(rural_access_scores)//4]:.2f}%")
    print(f"   • 50th percentile (median): {statistics.median(rural_access_scores):.2f}%")
    print(f"   • 75th percentile: {rural_access_scores[3*len(rural_access_scores)//4]:.2f}%")
    
    # Schools needing most help
    rural_schools_sorted = sorted(rural_schools, 
                                  key=lambda s: s.calculate_student_access_percentage())
    
    print(f"\n   📉 Bottom 5 Rural Schools (Need Most Support):")
    for i, school in enumerate(rural_schools_sorted[:5], 1):
        access = school.calculate_student_access_percentage()
        print(f"   {i}. {school.name} ({school.region.value}): {access:.1f}% access, "
              f"{school.student_count} students")
    
    return sim


def scenario_comparison():
    """
    Scenario 4: Multi-Scenario Comparison
    
    Runs multiple scenarios and compares outcomes side-by-side.
    """
    print("\n" + "="*80)
    print("SCENARIO 4: MULTI-SCENARIO COMPARISON")
    print("="*80)
    
    scenarios = {
        "Low Investment": [0.4, 0.5, 0.6, 0.7, 0.8],
        "Medium Investment": [0.8, 0.9, 1.0, 1.1, 1.2],
        "High Investment": [1.2, 1.4, 1.6, 1.8, 2.0]
    }
    
    results = {}
    
    for scenario_name, investment_schedule in scenarios.items():
        print(f"\n{'─'*80}")
        print(f"Running: {scenario_name}")
        print(f"{'─'*80}")
        
        sim = SimulationEngine(num_schools=30)  # Smaller for faster comparison
        sim.run_full_simulation(investment_schedule=investment_schedule)
        
        final_metrics = sim.metrics_history[-1]
        results[scenario_name] = {
            'student_access': final_metrics['student_access_percentage'],
            'cloud_adoption': final_metrics['cloud_adoption_rate'],
            'disparity': final_metrics['access_disparity'],
            'cost_efficiency': final_metrics['cost_efficiency']
        }
    
    # Comparison table
    print("\n" + "="*80)
    print("COMPARISON SUMMARY (Year 5)")
    print("="*80)
    print(f"\n{'Scenario':<20} {'Access %':<12} {'Adoption %':<12} {'Disparity':<12} {'Efficiency':<12}")
    print("─" * 80)
    
    for scenario_name, metrics in results.items():
        print(f"{scenario_name:<20} "
              f"{metrics['student_access']:>10.1f}% "
              f"{metrics['cloud_adoption']:>10.1f}% "
              f"{metrics['disparity']:>10.1f}% "
              f"{metrics['cost_efficiency']:>11.2f}")
    
    print("─" * 80)
    
    # Determine best scenario
    best_access = max(results.items(), key=lambda x: x[1]['student_access'])
    best_equity = min(results.items(), key=lambda x: x[1]['disparity'])
    
    print(f"\n🏆 WINNERS:")
    print(f"   Best Access Rate: {best_access[0]} ({best_access[1]['student_access']:.1f}%)")
    print(f"   Best Equity: {best_equity[0]} (disparity: {best_equity[1]['disparity']:.1f}%)")


def scenario_regional_analysis():
    """
    Scenario 5: Regional Deep Dive
    
    Analyzes performance across different regions of Cameroon.
    """
    print("\n" + "="*80)
    print("SCENARIO 5: REGIONAL ANALYSIS")
    print("="*80)
    
    sim = SimulationEngine(num_schools=100)  # Larger sample for regional analysis
    
    balanced_investment = [0.9, 1.0, 1.1, 1.3, 1.5]
    sim.run_full_simulation(investment_schedule=balanced_investment)
    
    # Group schools by region
    regional_data = {}
    
    for region in Region:
        region_schools = [s for s in sim.schools if s.region == region]
        
        if region_schools:
            avg_access = statistics.mean(
                s.calculate_student_access_percentage() for s in region_schools
            )
            total_students = sum(s.student_count for s in region_schools)
            
            regional_data[region.value] = {
                'schools': len(region_schools),
                'students': total_students,
                'avg_access': avg_access
            }
    
    # Sort by access rate
    sorted_regions = sorted(regional_data.items(), 
                          key=lambda x: x[1]['avg_access'], 
                          reverse=True)
    
    print(f"\n📍 REGIONAL PERFORMANCE RANKING (Year 5):")
    print(f"\n{'Rank':<6} {'Region':<20} {'Schools':<10} {'Students':<12} {'Avg Access':<12}")
    print("─" * 80)
    
    for rank, (region_name, data) in enumerate(sorted_regions, 1):
        print(f"{rank:<6} {region_name:<20} {data['schools']:<10} "
              f"{data['students']:<12,} {data['avg_access']:>10.1f}%")
    
    print("─" * 80)
    
    # Identify regions needing support
    low_performing = [r for r, d in sorted_regions if d['avg_access'] < 30]
    
    if low_performing:
        print(f"\n⚠️  REGIONS NEEDING PRIORITY SUPPORT (Access < 30%):")
        for region_name, data in low_performing:
            print(f"   • {region_name}: {data['avg_access']:.1f}% access, "
                  f"{data['students']:,} students affected")


def scenario_export_detailed_data():
    """
    Scenario 6: Data Export for External Analysis
    
    Demonstrates how to export detailed simulation data for further analysis
    in tools like Excel, R, or Tableau.
    """
    print("\n" + "="*80)
    print("SCENARIO 6: DATA EXPORT EXAMPLE")
    print("="*80)
    
    sim = SimulationEngine(num_schools=50)
    sim.run_full_simulation()
    
    # Export school-level data
    try:
        import csv
        
        # Export metrics history
        with open('metrics_history.csv', 'w', newline='', encoding='utf-8') as f:
            if sim.metrics_history:
                writer = csv.DictWriter(f, fieldnames=sim.metrics_history[0].keys())
                writer.writeheader()
                writer.writerows(sim.metrics_history)
        
        print("\n✓ Exported metrics_history.csv")
        
        # Export school details
        with open('school_details.csv', 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['name', 'location_type', 'region', 'student_count', 
                         'teacher_count', 'final_access_percentage', 'cloud_adoption_rate',
                         'internet_reliability', 'device_per_student']
            
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for school in sim.schools:
                writer.writerow({
                    'name': school.name,
                    'location_type': school.location_type.value,
                    'region': school.region.value,
                    'student_count': school.student_count,
                    'teacher_count': school.teacher_count,
                    'final_access_percentage': school.calculate_student_access_percentage(),
                    'cloud_adoption_rate': school.cloud_adoption_rate,
                    'internet_reliability': school.infrastructure.internet_reliability,
                    'device_per_student': school.infrastructure.device_per_student_ratio
                })
        
        print("✓ Exported school_details.csv")
        print("\n📊 Files ready for analysis in Excel, Tableau, or Python pandas!")
        
    except Exception as e:
        print(f"\n❌ Export error: {e}")
        print("Tip: Ensure you have write permissions in the current directory")


def main():
    """
    Main function to run all example scenarios.
    
    Users can comment out scenarios they don't want to run.
    """
    print("\n" + "="*80)
    print("CUSTOM SCENARIO EXAMPLES - CLOUD ADOPTION SIMULATION")
    print("="*80)
    print("\nThis module demonstrates various analysis scenarios.")
    print("Each scenario showcases different analytical approaches.\n")
    
    # Run scenarios (comment out any you don't want)
    
    print("\n[1/6] Running Aggressive Investment Scenario...")
    scenario_aggressive_investment()
    
    print("\n[2/6] Running Conservative Gradual Investment Scenario...")
    scenario_gradual_investment()
    
    print("\n[3/6] Running Rural-Focused Analysis...")
    scenario_rural_focused()
    
    print("\n[4/6] Running Multi-Scenario Comparison...")
    scenario_comparison()
    
    print("\n[5/6] Running Regional Analysis...")
    scenario_regional_analysis()
    
    print("\n[6/6] Running Data Export Example...")
    scenario_export_detailed_data()
    
    print("\n" + "="*80)
    print("ALL SCENARIOS COMPLETE")
    print("="*80)
    print("\nNext steps:")
    print("  • Review the console output above")
    print("  • Check generated CSV files for external analysis")
    print("  • Modify scenarios to test your own hypotheses")
    print("  • Integrate visualization.py for graphical analysis")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()