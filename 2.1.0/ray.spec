Name:           ray
Version:        2.1.0
Release:        2%{?dist}
Summary:        Parallel genome assemblies for parallel DNA sequencing

Group:          Applications/Engineering
License:        GPLv3
URL:            http://denovoassembler.sourceforge.net/
Source0:        http://downloads.sourceforge.net/denovoassembler/Ray-v%{version}.tar.bz2

BuildRequires:  openmpi-devel, bzip2-devel, zlib-devel
Requires:       openmpi

%description
Ray is a parallel software that computes de novo genome assemblies with   
next-generation sequencing data.
Ray is written in C++ and can run in parallel on numerous interconnected 
computers using the message-passing interface (MPI) standard.
Included:
 - Ray de novo assembly of single genomes
 - Ray Méta de novo assembly of metagenomes
 - Ray Communities microbe abundance + taxonomic profiling
 - Ray Ontologies gene ontology profiling

%package doc

Summary:        Documentation files
Group:          Documentation

%description doc
Ray is a parallel software that computes de novo genome assemblies with   
next-generation sequencing data.
Ray is written in C++ and can run in parallel on numerous interconnected 
computers using the message-passing interface (MPI) standard.

%package extra

Summary:        Scripts and XSL sheets for post-processing
Group:          Applications/Engineering

Requires:       python, R

%description extra
Ray is a parallel software that computes de novo genome assemblies with   
next-generation sequencing data.
Ray is written in C++ and can run in parallel on numerous interconnected 
computers using the message-passing interface (MPI) standard.

%prep
%setup -q -n Ray-v%{version}

%build
make HAVE_LIBZ=y HAVE_LIBBZ2=y 
module load mpi/openmpi-x86_64
help2man --no-info -n "assemble genomes in parallel using the message-passing interface" %{_builddir}/Ray-v%{version}/Ray > Ray.1

%install
rm -rf %{buildroot}

# ray
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_mandir}/man1
install -m 0755 Ray %{buildroot}/%{_bindir}/Ray
install -m 0644 Ray.1 %{buildroot}/%{_mandir}/man1/Ray.1

# doc (ray-doc)
mkdir -p %{buildroot}/%{_defaultdocdir}/ray/Documentation
mkdir -p %{buildroot}/%{_defaultdocdir}/ray/RayPlatform/Documentation
install -m 0644 Documentation/* %{buildroot}/%{_defaultdocdir}/ray/Documentation
install -m 0644 RayPlatform/Documentation/* %{buildroot}/%{_defaultdocdir}/ray/RayPlatform/Documentation

# extra (ray-extra)
mkdir -p %{buildroot}/%{_datadir}/ray
cp -r scripts %{buildroot}/%{_datadir}/ray
chmod 0755 %{buildroot}/%{_datadir}/ray/scripts

%clean
rm -rf %{buildroot}

%files
%doc MANUAL_PAGE.txt gpl-3.0.txt LICENSE.txt RayPlatform/lgpl-3.0.txt README.md
%{_bindir}/Ray
%{_mandir}/man1/Ray.1*

%files doc
%{_defaultdocdir}/ray/Documentation/*
%{_defaultdocdir}/ray/RayPlatform/Documentation/*

%files extra
%{_datadir}/ray/scripts/*

%changelog
* Fri Nov 3 2012 Sébastien Boisvert <sebastien.boisvert.3@ulaval.ca> - 2.1.0-2
- The Spec file was reviewed by Jussi Lehtola.
- Moved subpackage declarations to the top.

* Fri Nov 2 2012 Sébastien Boisvert <sebastien.boisvert.3@ulaval.ca> - 2.1.0-1
- This is the initial Ray package for Fedora

