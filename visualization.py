import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from typing import List, Dict
import numpy as np


class SimulationVisualizer:
    """
    Handles all visualization needs for the cloud adoption simulation.
    
    Provides methods to create various charts and graphs showing simulation
    results, trends, and comparative analysis.
    """
    
    def __init__(self, metrics_history: List[Dict[str, float]]):
        """
        Initialize visualizer with simulation metrics.
        
        Args:
            metrics_history: List of yearly metrics dictionaries from simulation
        """
        self.metrics_history = metrics_history
        self.years = [m['year'] for m in metrics_history]
        
        # Set professional style
        plt.style.use('seaborn-v0_8-darkgrid')
        self.colors = {
            'primary': '#2E86AB',
            'secondary': '#A23B72',
            'success': '#06A77D',
            'warning': '#F18F01',
            'danger': '#C73E1D',
            'urban': '#4ECDC4',
            'rural': '#FF6B6B'
        }
    
    def plot_comprehensive_dashboard(self, save_path: str = None) -> None:
        """
        Create a comprehensive dashboard with multiple subplots.
        
        Args:
            save_path: Optional path to save the figure (e.g., 'dashboard.png')
        """
        fig = plt.figure(figsize=(16, 12))
        gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.3, wspace=0.3)
        
        # Main title
        fig.suptitle('Cloud Computing Adoption in Cameroon Education System - 5 Year Analysis',
                    fontsize=16, fontweight='bold', y=0.98)
        
        # 1. Student Access Over Time
        ax1 = fig.add_subplot(gs[0, :2])
        self._plot_student_access_trend(ax1)
        
        # 2. Urban vs Rural Comparison
        ax2 = fig.add_subplot(gs[0, 2])
        self._plot_urban_rural_comparison(ax2)
        
        # 3. Infrastructure Progress
        ax3 = fig.add_subplot(gs[1, 0])
        self._plot_infrastructure_metrics(ax3)
        
        # 4. Teacher Readiness
        ax4 = fig.add_subplot(gs[1, 1])
        self._plot_teacher_metrics(ax4)
        
        # 5. Resource Availability
        ax5 = fig.add_subplot(gs[1, 2])
        self._plot_resource_availability(ax5)
        
        # 6. Cloud Adoption Rate
        ax6 = fig.add_subplot(gs[2, 0])
        self._plot_cloud_adoption(ax6)
        
        # 7. Cost Efficiency
        ax7 = fig.add_subplot(gs[2, 1])
        self._plot_cost_efficiency(ax7)
        
        # 8. Access Disparity Gap
        ax8 = fig.add_subplot(gs[2, 2])
        self._plot_disparity_gap(ax8)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"\n✓ Dashboard saved to: {save_path}")
        
        plt.show()
    
    def _plot_student_access_trend(self, ax) -> None:
        """Plot student access percentage over time with trend areas."""
        access = [m['student_access_percentage'] for m in self.metrics_history]
        urban = [m['urban_access'] for m in self.metrics_history]
        rural = [m['rural_access'] for m in self.metrics_history]
        
        ax.plot(self.years, access, marker='o', linewidth=2.5, 
               color=self.colors['primary'], label='Overall Access')
        ax.plot(self.years, urban, marker='s', linewidth=2, 
               color=self.colors['urban'], label='Urban', linestyle='--')
        ax.plot(self.years, rural, marker='^', linewidth=2, 
               color=self.colors['rural'], label='Rural', linestyle='--')
        
        ax.fill_between(self.years, access, alpha=0.3, color=self.colors['primary'])
        
        ax.set_xlabel('Year', fontweight='bold')
        ax.set_ylabel('Access Percentage (%)', fontweight='bold')
        ax.set_title('Student Cloud Platform Access Trend', fontweight='bold', pad=10)
        ax.legend(loc='upper left')
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 105)
    
    def _plot_urban_rural_comparison(self, ax) -> None:
        """Create bar comparison of final year urban vs rural metrics."""
        final_metrics = self.metrics_history[-1]
        
        categories = ['Access %']
        urban_vals = [final_metrics['urban_access']]
        rural_vals = [final_metrics['rural_access']]
        
        x = np.arange(len(categories))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, urban_vals, width, label='Urban',
                      color=self.colors['urban'], edgecolor='black', linewidth=1.2)
        bars2 = ax.bar(x + width/2, rural_vals, width, label='Rural',
                      color=self.colors['rural'], edgecolor='black', linewidth=1.2)
        
        ax.set_ylabel('Percentage (%)', fontweight='bold')
        ax.set_title('Urban vs Rural (Year 5)', fontweight='bold', pad=10)
        ax.set_xticks(x)
        ax.set_xticklabels(categories)
        ax.legend()
        ax.set_ylim(0, 100)
        
        # Add value labels on bars
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.1f}%', ha='center', va='bottom', fontsize=9)
    
    def _plot_infrastructure_metrics(self, ax) -> None:
        """Plot infrastructure improvement metrics."""
        internet = [m['avg_internet_reliability'] for m in self.metrics_history]
        
        ax.plot(self.years, internet, marker='o', linewidth=2.5,
               color=self.colors['success'])
        ax.fill_between(self.years, internet, alpha=0.3, color=self.colors['success'])
        
        ax.set_xlabel('Year', fontweight='bold')
        ax.set_ylabel('Reliability (%)', fontweight='bold')
        ax.set_title('Internet Reliability Progress', fontweight='bold', pad=10)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 105)
    
    def _plot_teacher_metrics(self, ax) -> None:
        """Plot teacher capability metrics."""
        literacy = [m['avg_teacher_digital_literacy'] for m in self.metrics_history]
        trained = [m['avg_teacher_cloud_trained'] for m in self.metrics_history]
        
        ax.plot(self.years, literacy, marker='s', linewidth=2,
               color=self.colors['primary'], label='Digital Literacy')
        ax.plot(self.years, trained, marker='^', linewidth=2,
               color=self.colors['secondary'], label='Cloud Trained')
        
        ax.set_xlabel('Year', fontweight='bold')
        ax.set_ylabel('Score / Percentage', fontweight='bold')
        ax.set_title('Teacher Readiness Metrics', fontweight='bold', pad=10)
        ax.legend(loc='upper left')
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 105)
    
    def _plot_resource_availability(self, ax) -> None:
        """Plot learning resource availability."""
        resources = [m['learning_resource_availability'] for m in self.metrics_history]
        
        ax.plot(self.years, resources, marker='D', linewidth=2.5,
               color=self.colors['warning'])
        ax.fill_between(self.years, resources, alpha=0.3, color=self.colors['warning'])
        
        ax.set_xlabel('Year', fontweight='bold')
        ax.set_ylabel('Availability (%)', fontweight='bold')
        ax.set_title('Learning Resource Availability', fontweight='bold', pad=10)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 105)
    
    def _plot_cloud_adoption(self, ax) -> None:
        """Plot cloud adoption rate with S-curve."""
        adoption = [m['cloud_adoption_rate'] for m in self.metrics_history]
        
        ax.plot(self.years, adoption, marker='o', linewidth=2.5,
               color=self.colors['primary'], markersize=8)
        ax.fill_between(self.years, adoption, alpha=0.3, color=self.colors['primary'])
        
        ax.set_xlabel('Year', fontweight='bold')
        ax.set_ylabel('Adoption Rate (%)', fontweight='bold')
        ax.set_title('Cloud Platform Adoption Rate', fontweight='bold', pad=10)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 105)
    
    def _plot_cost_efficiency(self, ax) -> None:
        """Plot cost efficiency trend."""
        efficiency = [m['cost_efficiency'] for m in self.metrics_history]
        
        ax.plot(self.years, efficiency, marker='s', linewidth=2.5,
               color=self.colors['success'])
        ax.fill_between(self.years, efficiency, alpha=0.3, color=self.colors['success'])
        
        ax.set_xlabel('Year', fontweight='bold')
        ax.set_ylabel('Access per M XAF', fontweight='bold')
        ax.set_title('Cost Efficiency Trend', fontweight='bold', pad=10)
        ax.grid(True, alpha=0.3)
    
    def _plot_disparity_gap(self, ax) -> None:
        """Plot urban-rural access disparity gap."""
        disparity = [m['access_disparity'] for m in self.metrics_history]
        
        colors = [self.colors['danger'] if d > 20 else self.colors['warning'] 
                 if d > 10 else self.colors['success'] for d in disparity]
        
        ax.bar(self.years, disparity, color=colors, edgecolor='black', linewidth=1.2)
        
        ax.axhline(y=20, color='red', linestyle='--', linewidth=1, alpha=0.5, label='High Disparity')
        ax.axhline(y=10, color='orange', linestyle='--', linewidth=1, alpha=0.5, label='Moderate')
        
        ax.set_xlabel('Year', fontweight='bold')
        ax.set_ylabel('Gap (%)', fontweight='bold')
        ax.set_title('Urban-Rural Access Disparity', fontweight='bold', pad=10)
        ax.legend(loc='upper right', fontsize=8)
        ax.grid(True, alpha=0.3, axis='y')
    
    def plot_year_over_year_comparison(self, save_path: str = None) -> None:
        """
        Create year-over-year comparison charts.
        
        Args:
            save_path: Optional path to save the figure
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Year-over-Year Comparison Analysis', 
                    fontsize=14, fontweight='bold')
        
        # Calculate year-over-year changes
        metrics_keys = ['student_access_percentage', 'cloud_adoption_rate',
                       'avg_teacher_cloud_trained', 'learning_resource_availability']
        titles = ['Student Access Growth', 'Cloud Adoption Growth',
                 'Teacher Training Growth', 'Resource Availability Growth']
        
        for idx, (key, title) in enumerate(zip(metrics_keys, titles)):
            ax = axes[idx // 2, idx % 2]
            
            values = [m[key] for m in self.metrics_history]
            yoy_change = [0] + [values[i] - values[i-1] for i in range(1, len(values))]
            
            colors = [self.colors['success'] if c >= 0 else self.colors['danger'] 
                     for c in yoy_change]
            
            ax.bar(self.years, yoy_change, color=colors, edgecolor='black', linewidth=1.2)
            ax.axhline(y=0, color='black', linewidth=1.5)
            ax.set_xlabel('Year', fontweight='bold')
            ax.set_ylabel('Change (%)', fontweight='bold')
            ax.set_title(title, fontweight='bold', pad=10)
            ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"\n✓ YoY comparison saved to: {save_path}")
        
        plt.show()


def visualize_simulation(simulation_engine):
    """
    Convenience function to visualize simulation results.
    
    Args:
        simulation_engine: SimulationEngine instance with completed simulation
    
    Usage:
        from main_simulation import SimulationEngine
        from visualization import visualize_simulation
        
        sim = SimulationEngine(num_schools=50)
        sim.run_full_simulation()
        visualize_simulation(sim)
    """
    if not simulation_engine.metrics_history:
        print("❌ Error: No simulation data found. Run simulation first.")
        return
    
    visualizer = SimulationVisualizer(simulation_engine.metrics_history)
    
    print("\n📊 Generating comprehensive dashboard...")
    visualizer.plot_comprehensive_dashboard(save_path='cloud_adoption_dashboard.png')
    
    print("\n📈 Generating year-over-year comparison...")
    visualizer.plot_year_over_year_comparison(save_path='yoy_comparison.png')
    
    print("\n✅ Visualization complete!")


# Example usage when run directly
if __name__ == "__main__":
    print("This is a visualization module.")
    print("\nTo use with simulation:")
    print("1. Run the main simulation first")
    print("2. Import: from visualization import visualize_simulation")
    print("3. Call: visualize_simulation(your_simulation_engine)")
    print("\nOr integrate into main.py as shown in the comprehensive example.")