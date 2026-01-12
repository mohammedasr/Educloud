import random
from dataclasses import dataclass, field
from typing import List, Dict, Tuple
from enum import Enum
import statistics


class LocationType(Enum):
    """Enumeration for school location types."""
    URBAN = "urban"
    RURAL = "rural"


class Region(Enum):
    """Major regions in Cameroon."""
    CENTRE = "Centre"
    LITTORAL = "Littoral"
    WEST = "West"
    NORTHWEST = "Northwest"
    SOUTHWEST = "Southwest"
    SOUTH = "South"
    EAST = "East"
    ADAMAWA = "Adamawa"
    NORTH = "North"
    FAR_NORTH = "Far North"


@dataclass
class Infrastructure:
    """
    Represents the technological infrastructure of a school.
    
    Attributes:
        internet_reliability: Percentage of uptime (0-100)
        bandwidth_mbps: Available bandwidth in Mbps
        power_availability: Percentage of time with electricity (0-100)
        device_per_student_ratio: Number of students per computing device
    """
    internet_reliability: float = 0.0
    bandwidth_mbps: float = 0.0
    power_availability: float = 0.0
    device_per_student_ratio: float = 100.0  # Higher is worse
    
    def update_with_investment(self, investment_multiplier: float) -> None:
        """Improve infrastructure based on investment level."""
        self.internet_reliability = min(100, self.internet_reliability + 
                                       random.uniform(3, 8) * investment_multiplier)
        self.bandwidth_mbps = min(100, self.bandwidth_mbps + 
                                 random.uniform(2, 6) * investment_multiplier)
        self.power_availability = min(100, self.power_availability + 
                                     random.uniform(2, 5) * investment_multiplier)
        self.device_per_student_ratio = max(1, self.device_per_student_ratio - 
                                           random.uniform(3, 7) * investment_multiplier)


@dataclass
class TeacherCapability:
    """
    Models teacher digital readiness and training levels.
    
    Attributes:
        digital_literacy_score: Overall digital competency (0-100)
        cloud_platform_trained: Percentage trained in cloud platforms (0-100)
        years_of_training: Average years of digital training
    """
    digital_literacy_score: float = 20.0
    cloud_platform_trained: float = 0.0
    years_of_training: float = 0.0
    
    def annual_training_update(self, training_intensity: float) -> None:
        """Update teacher capabilities based on annual training programs."""
        self.digital_literacy_score = min(100, self.digital_literacy_score + 
                                         random.uniform(5, 12) * training_intensity)
        self.cloud_platform_trained = min(100, self.cloud_platform_trained + 
                                         random.uniform(8, 15) * training_intensity)
        self.years_of_training += 0.5 * training_intensity


@dataclass
class School:
    """
    Represents an educational institution in Cameroon.
    
    Attributes:
        name: School identifier
        location_type: Urban or rural classification
        region: Geographic region in Cameroon
        student_count: Total number of students
        teacher_count: Total number of teachers
        infrastructure: Infrastructure object
        teacher_capability: TeacherCapability object
        cloud_adoption_rate: Percentage using cloud platforms (0-100)
        annual_budget: Annual budget in XAF (Central African Franc)
    """
    name: str
    location_type: LocationType
    region: Region
    student_count: int
    teacher_count: int
    infrastructure: Infrastructure = field(default_factory=Infrastructure)
    teacher_capability: TeacherCapability = field(default_factory=TeacherCapability)
    cloud_adoption_rate: float = 0.0
    annual_budget: float = 0.0
    
    def calculate_student_access_percentage(self) -> float:
        """
        Calculate the percentage of students with effective cloud access.
        
        Considers infrastructure quality, teacher readiness, and device availability.
        """
        # Infrastructure factor (weighted average)
        infra_factor = (
            self.infrastructure.internet_reliability * 0.4 +
            min(self.infrastructure.bandwidth_mbps * 2, 100) * 0.3 +
            self.infrastructure.power_availability * 0.3
        ) / 100
        
        # Device availability factor
        device_factor = max(0, 1 - (self.infrastructure.device_per_student_ratio / 100))
        
        # Teacher readiness factor
        teacher_factor = (
            self.teacher_capability.digital_literacy_score * 0.5 +
            self.teacher_capability.cloud_platform_trained * 0.5
        ) / 100
        
        # Combined access percentage
        access = (infra_factor * 0.4 + device_factor * 0.3 + teacher_factor * 0.3) * 100
        return min(100, access)
    
    def calculate_learning_resource_availability(self) -> float:
        """
        Calculate availability of digital learning resources.
        
        Returns: Score from 0-100 representing resource accessibility
        """
        base_availability = self.cloud_adoption_rate * 0.6
        infrastructure_boost = (self.infrastructure.bandwidth_mbps / 100) * 20
        teacher_boost = (self.teacher_capability.cloud_platform_trained / 100) * 20
        
        return min(100, base_availability + infrastructure_boost + teacher_boost)
    
    def evolve_year(self, govt_investment: float, year: int) -> None:
        """
        Simulate one year of evolution in cloud adoption.
        
        Args:
            govt_investment: Government investment multiplier (0.0-2.0)
            year: Current simulation year (1-5)
        """
        # Investment varies by location type
        location_multiplier = 1.5 if self.location_type == LocationType.URBAN else 0.7
        effective_investment = govt_investment * location_multiplier
        
        # Update infrastructure
        self.infrastructure.update_with_investment(effective_investment)
        
        # Update teacher capability
        training_intensity = effective_investment * random.uniform(0.8, 1.2)
        self.teacher_capability.annual_training_update(training_intensity)
        
        # Update cloud adoption rate (S-curve adoption model)
        growth_potential = 100 - self.cloud_adoption_rate
        student_access = self.calculate_student_access_percentage()
        adoption_growth = (growth_potential / 100) * (student_access / 50) * random.uniform(8, 15)
        self.cloud_adoption_rate = min(100, self.cloud_adoption_rate + adoption_growth)
        
        # Random events (challenges and opportunities)
        self._apply_random_events(year)
    
    def _apply_random_events(self, year: int) -> None:
        """Apply random positive or negative events affecting the school."""
        event_roll = random.random()
        
        # 20% chance of a significant event
        if event_roll < 0.20:
            if random.random() < 0.6:  # 60% positive, 40% negative
                # Positive event: NGO donation, partnership, etc.
                self.infrastructure.bandwidth_mbps = min(100, 
                    self.infrastructure.bandwidth_mbps + random.uniform(5, 15))
                self.infrastructure.device_per_student_ratio = max(1,
                    self.infrastructure.device_per_student_ratio - random.uniform(5, 10))
            else:
                # Negative event: equipment theft, infrastructure damage, etc.
                self.infrastructure.internet_reliability = max(0,
                    self.infrastructure.internet_reliability - random.uniform(5, 15))


class SimulationEngine:
    """
    Core simulation engine for cloud adoption modeling.
    
    Manages the entire ecosystem of schools, government policies, and metrics.
    """
    
    def __init__(self, num_schools: int = 50):
        """
        Initialize the simulation with a specified number of schools.
        
        Args:
            num_schools: Total number of schools to simulate (default: 50)
        """
        self.schools: List[School] = []
        self.num_schools = num_schools
        self.current_year = 0
        self.government_budget_per_year: List[float] = []
        self.metrics_history: List[Dict[str, float]] = []
        
        self._generate_schools()
    
    def _generate_schools(self) -> None:
        """Generate a realistic distribution of schools across Cameroon."""
        regions = list(Region)
        
        for i in range(self.num_schools):
            # 60% urban, 40% rural (realistic for Cameroon)
            location_type = (LocationType.URBAN if random.random() < 0.6 
                           else LocationType.RURAL)
            
            region = random.choice(regions)
            
            # School size varies by location
            if location_type == LocationType.URBAN:
                student_count = random.randint(500, 2000)
                teacher_count = random.randint(20, 80)
                budget_base = random.uniform(15_000_000, 50_000_000)  # XAF
            else:
                student_count = random.randint(100, 600)
                teacher_count = random.randint(8, 30)
                budget_base = random.uniform(3_000_000, 15_000_000)  # XAF
            
            # Initialize infrastructure based on location
            infrastructure = self._create_initial_infrastructure(location_type)
            
            # Initialize teacher capability (lower in rural areas)
            teacher_cap = TeacherCapability(
                digital_literacy_score=random.uniform(15, 35) if location_type == LocationType.URBAN 
                                      else random.uniform(5, 20),
                cloud_platform_trained=random.uniform(0, 10) if location_type == LocationType.URBAN 
                                      else random.uniform(0, 3)
            )
            
            school = School(
                name=f"School_{location_type.value[:3].upper()}_{i+1:03d}",
                location_type=location_type,
                region=region,
                student_count=student_count,
                teacher_count=teacher_count,
                infrastructure=infrastructure,
                teacher_capability=teacher_cap,
                cloud_adoption_rate=random.uniform(0, 5),
                annual_budget=budget_base
            )
            
            self.schools.append(school)
    
    def _create_initial_infrastructure(self, location_type: LocationType) -> Infrastructure:
        """Create initial infrastructure based on location type."""
        if location_type == LocationType.URBAN:
            return Infrastructure(
                internet_reliability=random.uniform(40, 70),
                bandwidth_mbps=random.uniform(5, 20),
                power_availability=random.uniform(60, 85),
                device_per_student_ratio=random.uniform(20, 50)
            )
        else:  # Rural
            return Infrastructure(
                internet_reliability=random.uniform(10, 35),
                bandwidth_mbps=random.uniform(0.5, 5),
                power_availability=random.uniform(20, 50),
                device_per_student_ratio=random.uniform(50, 100)
            )
    
    def simulate_year(self, govt_investment_level: float) -> Dict[str, float]:
        """
        Simulate one year across all schools.
        
        Args:
            govt_investment_level: Government investment multiplier (0.0-2.0)
                                  1.0 = baseline, 2.0 = doubled investment
        
        Returns:
            Dictionary containing yearly metrics
        """
        self.current_year += 1
        self.government_budget_per_year.append(govt_investment_level)
        
        # Evolve each school
        for school in self.schools:
            school.evolve_year(govt_investment_level, self.current_year)
        
        # Calculate system-wide metrics
        metrics = self._calculate_system_metrics()
        self.metrics_history.append(metrics)
        
        return metrics
    
    def _calculate_system_metrics(self) -> Dict[str, float]:
        """Calculate comprehensive system-wide metrics."""
        total_students = sum(s.student_count for s in self.schools)
        
        # Weighted averages by student population
        student_access_weighted = sum(
            s.calculate_student_access_percentage() * s.student_count 
            for s in self.schools
        ) / total_students
        
        resource_availability_weighted = sum(
            s.calculate_learning_resource_availability() * s.student_count 
            for s in self.schools
        ) / total_students
        
        adoption_rate_weighted = sum(
            s.cloud_adoption_rate * s.student_count 
            for s in self.schools
        ) / total_students
        
        # Urban vs Rural metrics
        urban_schools = [s for s in self.schools if s.location_type == LocationType.URBAN]
        rural_schools = [s for s in self.schools if s.location_type == LocationType.RURAL]
        
        urban_access = statistics.mean(
            s.calculate_student_access_percentage() for s in urban_schools
        ) if urban_schools else 0
        
        rural_access = statistics.mean(
            s.calculate_student_access_percentage() for s in rural_schools
        ) if rural_schools else 0
        
        # Infrastructure metrics
        avg_internet_reliability = statistics.mean(
            s.infrastructure.internet_reliability for s in self.schools
        )
        
        avg_device_ratio = statistics.mean(
            s.infrastructure.device_per_student_ratio for s in self.schools
        )
        
        # Teacher readiness
        avg_teacher_literacy = statistics.mean(
            s.teacher_capability.digital_literacy_score for s in self.schools
        )
        
        avg_teacher_trained = statistics.mean(
            s.teacher_capability.cloud_platform_trained for s in self.schools
        )
        
        # Cost efficiency (access per unit investment)
        total_budget = sum(s.annual_budget for s in self.schools)
        cost_efficiency = (student_access_weighted / (total_budget / 1_000_000)) if total_budget > 0 else 0
        
        return {
            "year": self.current_year,
            "student_access_percentage": student_access_weighted,
            "learning_resource_availability": resource_availability_weighted,
            "cloud_adoption_rate": adoption_rate_weighted,
            "urban_access": urban_access,
            "rural_access": rural_access,
            "access_disparity": urban_access - rural_access,
            "avg_internet_reliability": avg_internet_reliability,
            "avg_device_per_student": avg_device_ratio,
            "avg_teacher_digital_literacy": avg_teacher_literacy,
            "avg_teacher_cloud_trained": avg_teacher_trained,
            "cost_efficiency": cost_efficiency,
            "total_students": total_students
        }
    
    def run_full_simulation(self, investment_schedule: List[float] = None) -> None:
        """
        Run the complete 5-year simulation.
        
        Args:
            investment_schedule: List of 5 investment multipliers, one per year.
                               If None, uses a default realistic schedule.
        """
        if investment_schedule is None:
            # Default: gradual increase in investment over 5 years
            investment_schedule = [0.6, 0.8, 1.0, 1.2, 1.4]
        
        if len(investment_schedule) != 5:
            raise ValueError("Investment schedule must have exactly 5 values")
        
        print("\n" + "="*80)
        print("CLOUD COMPUTING ADOPTION SIMULATION - CAMEROON EDUCATION SYSTEM")
        print("="*80)
        print(f"\nSimulating {self.num_schools} schools over 5 years")
        print(f"Total students in system: {sum(s.student_count for s in self.schools):,}")
        print(f"Urban schools: {sum(1 for s in self.schools if s.location_type == LocationType.URBAN)}")
        print(f"Rural schools: {sum(1 for s in self.schools if s.location_type == LocationType.RURAL)}")
        print("\n" + "-"*80)
        
        for year_idx, investment in enumerate(investment_schedule):
            metrics = self.simulate_year(investment)
            self._print_year_summary(metrics, investment)
        
        self._print_final_analysis()
    
    def _print_year_summary(self, metrics: Dict[str, float], investment: float) -> None:
        """Print formatted summary for a single year."""
        print(f"\n{'YEAR ' + str(metrics['year']):.^80}")
        print(f"Government Investment Level: {investment:.1f}x baseline")
        print("-"*80)
        
        print(f"\n📊 OVERALL METRICS:")
        print(f"  • Student Access to Cloud Platforms:    {metrics['student_access_percentage']:6.2f}%")
        print(f"  • Learning Resource Availability:       {metrics['learning_resource_availability']:6.2f}%")
        print(f"  • Cloud Adoption Rate:                  {metrics['cloud_adoption_rate']:6.2f}%")
        
        print(f"\n🏙️  URBAN VS RURAL DIVIDE:")
        print(f"  • Urban School Access:                  {metrics['urban_access']:6.2f}%")
        print(f"  • Rural School Access:                  {metrics['rural_access']:6.2f}%")
        print(f"  • Access Disparity Gap:                 {metrics['access_disparity']:6.2f}%")
        
        print(f"\n🔧 INFRASTRUCTURE:")
        print(f"  • Average Internet Reliability:         {metrics['avg_internet_reliability']:6.2f}%")
        print(f"  • Average Students per Device:          {metrics['avg_device_per_student']:6.2f}")
        
        print(f"\n👨‍🏫 TEACHER READINESS:")
        print(f"  • Digital Literacy Score:               {metrics['avg_teacher_digital_literacy']:6.2f}/100")
        print(f"  • Cloud Platform Training:              {metrics['avg_teacher_cloud_trained']:6.2f}%")
        
        print(f"\n💰 EFFICIENCY:")
        print(f"  • Cost Efficiency (access/M XAF):       {metrics['cost_efficiency']:6.2f}")
        
        print("-"*80)
    
    def _print_final_analysis(self) -> None:
        """Print comprehensive final analysis after 5-year simulation."""
        print("\n" + "="*80)
        print("5-YEAR SIMULATION COMPLETE - FINAL ANALYSIS")
        print("="*80)
        
        first_year = self.metrics_history[0]
        last_year = self.metrics_history[-1]
        
        print(f"\n📈 GROWTH OVER 5 YEARS:")
        print(f"  • Student Access:           {first_year['student_access_percentage']:6.2f}% → "
              f"{last_year['student_access_percentage']:6.2f}% "
              f"(+{last_year['student_access_percentage'] - first_year['student_access_percentage']:5.2f}%)")
        
        print(f"  • Learning Resources:       {first_year['learning_resource_availability']:6.2f}% → "
              f"{last_year['learning_resource_availability']:6.2f}% "
              f"(+{last_year['learning_resource_availability'] - first_year['learning_resource_availability']:5.2f}%)")
        
        print(f"  • Cloud Adoption:           {first_year['cloud_adoption_rate']:6.2f}% → "
              f"{last_year['cloud_adoption_rate']:6.2f}% "
              f"(+{last_year['cloud_adoption_rate'] - first_year['cloud_adoption_rate']:5.2f}%)")
        
        print(f"\n🌍 EQUITY PROGRESS:")
        print(f"  • Initial Disparity:        {first_year['access_disparity']:6.2f}%")
        print(f"  • Final Disparity:          {last_year['access_disparity']:6.2f}%")
        disparity_change = last_year['access_disparity'] - first_year['access_disparity']
        print(f"  • Change:                   {disparity_change:+6.2f}% "
              f"({'IMPROVED' if disparity_change < 0 else 'WORSENED'})")
        
        print(f"\n📚 TEACHER DEVELOPMENT:")
        print(f"  • Digital Literacy:         {first_year['avg_teacher_digital_literacy']:6.2f} → "
              f"{last_year['avg_teacher_digital_literacy']:6.2f} "
              f"(+{last_year['avg_teacher_digital_literacy'] - first_year['avg_teacher_digital_literacy']:5.2f})")
        
        print(f"  • Cloud Training:           {first_year['avg_teacher_cloud_trained']:6.2f}% → "
              f"{last_year['avg_teacher_cloud_trained']:6.2f}% "
              f"(+{last_year['avg_teacher_cloud_trained'] - first_year['avg_teacher_cloud_trained']:5.2f}%)")
        
        # Success assessment
        print(f"\n🎯 SUCCESS INDICATORS:")
        success_count = 0
        total_checks = 5
        
        checks = [
            (last_year['student_access_percentage'] > 50, 
             f"  {'✓' if last_year['student_access_percentage'] > 50 else '✗'} "
             f"Student access >50%: {last_year['student_access_percentage']:.1f}%"),
            
            (last_year['access_disparity'] < first_year['access_disparity'],
             f"  {'✓' if last_year['access_disparity'] < first_year['access_disparity'] else '✗'} "
             f"Reduced urban-rural gap: {disparity_change:+.1f}%"),
            
            (last_year['avg_teacher_cloud_trained'] > 60,
             f"  {'✓' if last_year['avg_teacher_cloud_trained'] > 60 else '✗'} "
             f"Teacher training >60%: {last_year['avg_teacher_cloud_trained']:.1f}%"),
            
            (last_year['cloud_adoption_rate'] > 40,
             f"  {'✓' if last_year['cloud_adoption_rate'] > 40 else '✗'} "
             f"Cloud adoption >40%: {last_year['cloud_adoption_rate']:.1f}%"),
            
            (last_year['cost_efficiency'] > first_year['cost_efficiency'],
             f"  {'✓' if last_year['cost_efficiency'] > first_year['cost_efficiency'] else '✗'} "
             f"Improved cost efficiency: {last_year['cost_efficiency']:.2f}")
        ]
        
        for passed, message in checks:
            print(message)
            if passed:
                success_count += 1
        
        print(f"\nOverall Success Rate: {success_count}/{total_checks} "
              f"({100*success_count/total_checks:.0f}%)")
        
        print("\n" + "="*80)
        print("Simulation data available in simulation.metrics_history for further analysis")
        print("="*80 + "\n")


def main():
    """Main entry point for the simulation program."""
    # Set random seed for reproducibility (optional - remove for true randomness)
    random.seed(42)
    
    # Create simulation with 50 schools
    simulation = SimulationEngine(num_schools=50)
    
    # Define investment schedule
    # Year 1-2: Low investment (establishing foundation)
    # Year 3: Moderate investment
    # Year 4-5: Higher investment (scaling phase)
    investment_schedule = [0.7, 0.9, 1.1, 1.4, 1.6]
    
    # Run the complete 5-year simulation
    simulation.run_full_simulation(investment_schedule)
    
    # Optional: Access raw data for custom analysis
    print("\n📊 Sample raw data access:")
    print(f"Year 3 metrics: {simulation.metrics_history[2]}")
    print(f"\nFirst 3 schools summary:")
    for i, school in enumerate(simulation.schools[:3]):
        print(f"  {school.name}: {school.calculate_student_access_percentage():.1f}% access, "
              f"{school.student_count} students, {school.location_type.value}")


if __name__ == "__main__":
    main()