from main_app.models import Astronaut, Mission, Spacecraft
from django.db.models import Count, Sum, Q


def get_last_completed_mission():
    mission = Mission.objects.filter(status='Completed').order_by('-launch_date').first()

    if not mission:
        return "No data."

    commander_name = mission.commander.name if mission.commander else "TBA"
    astronauts = mission.astronauts.all().order_by('name')
    astronaut_names = ", ".join([astronaut.name for astronaut in astronauts])
    total_spacewalks = astronauts.aggregate(total=Sum('spacewalks'))['total']

    return (f"The last completed mission is: {mission.name}. Commander: {commander_name}. "
            f"Astronauts: {astronaut_names}. Spacecraft: {mission.spacecraft.name}. "
            f"Total spacewalks: {total_spacewalks}.")

def get_most_used_spacecraft():
    spacecraft = Spacecraft.objects.annotate(num_missions=Count('mission')).order_by('-num_missions', 'name').first()

    if not spacecraft or spacecraft.num_missions == 0:
        return "No data."

    unique_astronauts = Astronaut.objects.filter(missions__spacecraft=spacecraft).distinct().count()

    return (f"The most used spacecraft is: {spacecraft.name}, manufactured by {spacecraft.manufacturer}, "
            f"used in {spacecraft.num_missions} missions, astronauts on missions: {unique_astronauts}.")

def decrease_spacecrafts_weight():
    spacecrafts = Spacecraft.objects.filter(mission__status='Planned').distinct().filter(weight__gte=200.0)

    if not spacecrafts.exists():
        return "No changes in weight."

    for spacecraft in spacecrafts:
        spacecraft.weight -= 200.0
        spacecraft.save()

    total_weight = Spacecraft.objects.aggregate(avg_weight=Sum('weight') / Count('id'))['avg_weight']
    avg_weight = round(total_weight, 1)

    return (f"The weight of {spacecrafts.count()} spacecrafts has been decreased. "
            f"The new average weight of all spacecrafts is {avg_weight}kg")
