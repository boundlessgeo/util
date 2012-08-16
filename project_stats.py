# -*- coding: utf-8 -*-
# Generates commit stats files for each project.  Assumes git repo clones relative to pwd.

import subprocess

projects = ['postgis', 'geotools', 'geoserver', 'geowebcache', 'openlayers', 'geoext']

years = range(2007, 2013)

# Keyed by proper name.  Values are list of git author names.
aliases = {
    'Andrea Aime': ['aaime'],
    'Andreas Hocevar': ['ahocevar'],
    'Antoine Abt': ['aabt'],
    'Bart van den Eijnden': ['bartvde'],
    'Christian Mayer': ['chrismayer'],
    'Christopher Schmidt': ['crschmidt'],
    'David Winslow': ['dwinslow', 'dwins'],
    'Erik Uzureau': ['euzuro'],
    'François Van Der Biest': ['fvanderbiest'],
    'Frédéric Junod': ['fredj', 'Frederic Junod'],
    'Gabriel Roldan': ['groldan'],
    'Ian Schneider': ['ischneider', 'ianschneider'],
    'Jody Garnett': ['jgarnett'],
    'John Frank': ['jrf'],
    'Justin Deoliveira': ['jdeolive'],
    'Niels Charlier': ['nielscharlier', 'NielsCharlier'],
    'Martin Davis': ['mdavis'],
    'Mike Pumphrey': ['bmmpxf'],
    'Pierre Giraud': ['Pierre GIRAUD', 'pgiraud'],
    'Sebastian Benthall': ['sbenthall'],
    'Tim Coulter': ['tcoulter'],
    'Tim Schaub': ['tschaub'],
}

index = dict()
for (name, names) in aliases.items():
    for alias in names:
        index[alias] = name

for project in projects:
    commits = dict()
    for year in years:
        command = 'cd %s; git log --after={%d-01-01} --before={%d-01-01} --pretty=format:%%aN --no-merges'  % (project, year, year+1)
        log = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE).communicate()[0].split('\n')

        for alias in filter(None, log):
            if index.has_key(alias):
                name = index[alias]
            else:
                name = alias
            if not commits.has_key(name):
                commits[name] = {year: 1}
            else:
                yearly_commits = commits[name]
                if not yearly_commits.has_key(year):
                    yearly_commits[year] = 1
                else:
                    yearly_commits[year] += 1

    with open('%s_stats.txt' % (project,), 'w') as f:
        row = 'name\t%s\n' % '\t'.join(str(year) for year in years)
        f.write(row)
        for name in sorted(commits.keys()):
            yearly_commits = commits[name]
            row = '%s\t%s\n' % (name, '\t'.join(str(yearly_commits[year]) if yearly_commits.has_key(year) else '0' for year in years))
            f.write(row)

