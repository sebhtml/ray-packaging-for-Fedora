Name:           Ray
Version:        2.1.0
Release:        5%{?dist}
Summary:        Parallel genome assemblies for parallel DNA sequencing

Group:          Applications/Engineering
License:        GPLv3
URL:            http://denovoassembler.sourceforge.net/
Source0:        http://downloads.sourceforge.net/denovoassembler/%{name}-v%{version}.tar.bz2
Patch0:         Ray.manpage.patch

BuildRequires:  openmpi-devel, bzip2-devel, zlib-devel, mpich2-devel

%description
%{name} is a parallel software that computes de novo genome assemblies with   
next-generation sequencing data.
%{name} is written in C++ and can run in parallel on numerous interconnected 
computers using the message-passing interface (MPI) standard.
Included:
 - %{name} de novo assembly of single genomes
 - %{name} Méta de novo assembly of metagenomes
 - %{name} Communities microbe abundance + taxonomic profiling
 - %{name} Ontologies gene ontology profiling

%package common
Summary:        Parallel genome assemblies for parallel DNA sequencing
Group:          Applications/Engineering

%description common
%{name} is a parallel software that computes de novo genome assemblies with   
next-generation sequencing data.
%{name} is written in C++ and can run in parallel on numerous interconnected 
computers using the message-passing interface (MPI) standard.
This sub-package contains common files for Ray.

%package openmpi
Summary:        %{name} package for Open-MPI
Group:          Applications/Engineering
Requires:       openmpi, %{name}-common

%description openmpi
%{name} is a parallel software that computes de novo genome assemblies with   
next-generation sequencing data.
%{name} is written in C++ and can run in parallel on numerous interconnected 
computers using the message-passing interface (MPI) standard.
This sub-package enables parallel computation using openmpi.

%package mpich2
Summary:        %{name} package for MPICH2
Group:          Applications/Engineering
Requires:       mpich2, %{name}-common

%description mpich2
%{name} is a parallel software that computes de novo genome assemblies with   
next-generation sequencing data.
%{name} is written in C++ and can run in parallel on numerous interconnected 
computers using the message-passing interface (MPI) standard.
This sub-package enables parallel computation using mpich2.

%package doc
Summary:        Documentation files
Group:          Documentation
Requires:       %{name}-common

%description doc
%{name} is a parallel software that computes de novo genome assemblies with   
next-generation sequencing data.
%{name} is written in C++ and can run in parallel on numerous interconnected 
computers using the message-passing interface (MPI) standard.
This sub-package includes documentation files.

%package extra
Summary:        Scripts and XSL sheets for post-processing
Group:          Applications/Engineering
Requires:       python, R, %{name}-common

%description extra
%{name} is a parallel software that computes de novo genome assemblies with   
next-generation sequencing data.
%{name} is written in C++ and can run in parallel on numerous interconnected 
computers using the message-passing interface (MPI) standard.
This sub-package contains scripts and XSL sheets for post-processing.

%prep
%setup -q -n %{name}-v%{version}
%patch0

%build
CXXFLAGS="%{optflags} -D MAXKMERLENGTH=32 -D HAVE_LIBZ -D HAVE_LIBBZ2 -D "
CXXFLAGS+="RAY_VERSION=\\\\\\\"2.1.0\\\\\\\" "
CXXFLAGS+="-D RAYPLATFORM_VERSION=\\\\\\\"1.1.0\\\\\\\" -I . -I ../%{name}Platform"

%{_openmpi_load}
make CXXFLAGS="$CXXFLAGS" HAVE_LIBBZ2=y HAVE_LIBZ=y
cp %{name} %{name}$MPI_SUFFIX

cp README.md README
cp %{name}Platform/README README.%{name}Platform
cp %{name}Platform/AUTHORS AUTHORS.%{name}Platform

make clean
%{_openmpi_unload}

%{_mpich2_load}
make CXXFLAGS="$CXXFLAGS" HAVE_LIBBZ2=y HAVE_LIBZ=y
cp %{name} %{name}$MPI_SUFFIX
make clean
%{_mpich2_unload}

%install
rm -rf %{buildroot}

# Ray-common
mkdir -p %{buildroot}%{_mandir}/man1
install -m 0644 %{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1

# Ray-openmpi
%{_openmpi_load}
mkdir -p %{buildroot}$MPI_BIN
install -m 0755 %{name}$MPI_SUFFIX %{buildroot}$MPI_BIN
%{_openmpi_unload}

# Ray-mpich2
%{_mpich2_load}
mkdir -p %{buildroot}$MPI_BIN
install -m 0755 %{name}$MPI_SUFFIX %{buildroot}$MPI_BIN
%{_mpich2_unload}

# Ray-doc
mkdir doc
cp -ar %{name}Platform/Documentation/ doc/%{name}Platform
chmod 644 doc/%{name}Platform/*
chmod 644 Documentation/*

# Ray-extra
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -r scripts %{buildroot}%{_datadir}/%{name}
chmod 0755 %{buildroot}%{_datadir}/%{name}/scripts

%clean
rm -rf %{buildroot}

%files common
%doc MANUAL_PAGE.txt gpl-3.0.txt LICENSE.txt 
%doc %{name}Platform/lgpl-3.0.txt
%doc AUTHORS AUTHORS.%{name}Platform
%doc README README.%{name}Platform
%{_mandir}/man1/%{name}.1*

%files openmpi
%{_libdir}/openmpi/bin/%{name}*

%files mpich2
%{_libdir}/mpich2/bin/%{name}*

%files doc
%doc Documentation/*
%doc doc/%{name}Platform/

%files extra
%{_datadir}/%{name}/

%changelog

* Fri Nov 29 2012 Sébastien Boisvert <sebastien.boisvert.3@ulaval.ca> - 2.1.0-5
- Added a patch for the man page

* Fri Nov 5 2012 Sébastien Boisvert <sebastien.boisvert.3@ulaval.ca> - 2.1.0-4
- The man page encoding is en_US.UTF-8
- Added more specific descriptions

* Fri Nov 4 2012 Sébastien Boisvert <sebastien.boisvert.3@ulaval.ca> - 2.1.0-3
- Changed the package name from ray to Ray
- Renamed README.md to README
- Added AUTHORS, README.RayPlatform, AUTHORS.RayPlatform

* Fri Nov 4 2012 Sébastien Boisvert <sebastien.boisvert.3@ulaval.ca> - 2.1.0-2
- Added build dependency help2man 
- Added OMPI_MCA_orte_rsh_agent to pass mock builds

* Fri Nov 3 2012 Sébastien Boisvert <sebastien.boisvert.3@ulaval.ca> - 2.1.0-1

- The Spec file was (informally) reviewed by Jussi Lehtola
- Moved sub-package declarations to the top
- Added sub-packages common, openmpi, mpich2
- Removed useless '/' after buildroot
- Fixed the packaging of Documentation
- Removed symbols that are not U.S. American English from man page
- Added Fedora compilation flags (optflags)
- The Spec file was (informally) reviewed a second time by Jussi Lehtola
- CXXFLAGS was shortened
- Replacement of non-ASCII symbols is more compact with sed
- ray-extra now ships _datadir/ray/ instead of _datadir/ray/scripts/.
- This is the initial Ray package for Fedora
