Name:           ray
Version:        2.1.0
Release:        2%{?dist}
Summary:        Parallel genome assemblies for parallel DNA sequencing

Group:          Applications/Engineering
License:        GPLv3
URL:            http://denovoassembler.sourceforge.net/
Source0:        http://downloads.sourceforge.net/denovoassembler/Ray-v%{version}.tar.bz2

BuildRequires:  openmpi-devel, bzip2-devel, zlib-devel, mpich2-devel

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

%package common

Summary:        Parallel genome assemblies for parallel DNA sequencing
Group:          Applications/Engineering

%description common
Ray is a parallel software that computes de novo genome assemblies with   
next-generation sequencing data.
Ray is written in C++ and can run in parallel on numerous interconnected 
computers using the message-passing interface (MPI) standard.

%package openmpi

Summary:        Ray package for Open-MPI
Group:          Applications/Engineering
Requires:       openmpi, ray-common

%description openmpi
Ray is a parallel software that computes de novo genome assemblies with   
next-generation sequencing data.
Ray is written in C++ and can run in parallel on numerous interconnected 
computers using the message-passing interface (MPI) standard.

%package mpich2

Summary:        Ray package for MPICH2
Group:          Applications/Engineering
Requires:       mpich2, ray-common

%description mpich2
Ray is a parallel software that computes de novo genome assemblies with   
next-generation sequencing data.
Ray is written in C++ and can run in parallel on numerous interconnected 
computers using the message-passing interface (MPI) standard.



%package doc

Summary:        Documentation files
Group:          Documentation
Requires:       ray-common

%description doc
Ray is a parallel software that computes de novo genome assemblies with   
next-generation sequencing data.
Ray is written in C++ and can run in parallel on numerous interconnected 
computers using the message-passing interface (MPI) standard.

%package extra

Summary:        Scripts and XSL sheets for post-processing
Group:          Applications/Engineering
Requires:       python, R, ray-common

%description extra
Ray is a parallel software that computes de novo genome assemblies with   
next-generation sequencing data.
Ray is written in C++ and can run in parallel on numerous interconnected 
computers using the message-passing interface (MPI) standard.

%prep
%setup -q -n Ray-v%{version}

%build
%{_openmpi_load}
make HAVE_LIBZ=y HAVE_LIBBZ2=y 
cp Ray Ray$MPI_SUFFIX
help2man --no-info -n "assemble genomes in parallel using the message-passing interface" %{_builddir}/Ray-v%{version}/Ray > Ray.1
make clean
%{_openmpi_unload}

%{_mpich2_load}
make HAVE_LIBZ=y HAVE_LIBBZ2=y 
cp Ray Ray$MPI_SUFFIX
make clean
%{_mpich2_unload}

%install
rm -rf %{buildroot}

# ray
mkdir -p %{buildroot}%{_mandir}/man1
install -m 0644 Ray.1 %{buildroot}%{_mandir}/man1/Ray.1

# ray openmpi
%{_openmpi_load}
mkdir -p %{buildroot}$MPI_BIN
install -m 0755 Ray$MPI_SUFFIX %{buildroot}$MPI_BIN
%{_openmpi_unload}

# ray mpich2
%{_mpich2_load}
mkdir -p %{buildroot}$MPI_BIN
install -m 0755 Ray$MPI_SUFFIX %{buildroot}$MPI_BIN
%{_mpich2_unload}

# doc (ray-doc)
mkdir -p %{buildroot}%{_defaultdocdir}/ray/Documentation
mkdir -p %{buildroot}%{_defaultdocdir}/ray/RayPlatform/Documentation
install -m 0644 Documentation/* %{buildroot}%{_defaultdocdir}/ray/Documentation
install -m 0644 RayPlatform/Documentation/* %{buildroot}%{_defaultdocdir}/ray/RayPlatform/Documentation

# extra (ray-extra)
mkdir -p %{buildroot}%{_datadir}/ray
cp -r scripts %{buildroot}%{_datadir}/ray
chmod 0755 %{buildroot}%{_datadir}/ray/scripts

%clean
rm -rf %{buildroot}

%files common
%doc MANUAL_PAGE.txt gpl-3.0.txt LICENSE.txt RayPlatform/lgpl-3.0.txt README.md
%{_mandir}/man1/Ray.1*

%files openmpi
%{_libdir}/openmpi/bin/Ray*

%files mpich2
%{_libdir}/mpich2/bin/Ray*

%files doc
%{_defaultdocdir}/ray/Documentation/*
%{_defaultdocdir}/ray/RayPlatform/Documentation/*

%files extra
%{_datadir}/ray/scripts/*

%changelog
* Fri Nov 3 2012 Sébastien Boisvert <sebastien.boisvert.3@ulaval.ca> - 2.1.0-2
- The Spec file was reviewed by Jussi Lehtola
- Moved subpackage declarations to the top
- Added subpackages common, openmpi, mpich2
- Removed useless '/' after %{buildroot}

* Fri Nov 2 2012 Sébastien Boisvert <sebastien.boisvert.3@ulaval.ca> - 2.1.0-1
- This is the initial Ray package for Fedora

