%{!?ruby_sitelib: %global ruby_sitelib %(ruby -rrbconfig -e 'puts Config::CONFIG["sitelibdir"] ')}
%{!?ruby_sitearch: %global ruby_sitearch %(ruby -rrbconfig -e 'puts Config::CONFIG["sitearchdir"] ')}
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%global php_extdir  %(php-config --extension-dir 2>/dev/null || echo "undefined")
%global php_version %(php-config --version 2>/dev/null || echo 0)

Summary:        Toolkit for broadcasters, video editors, media players, transcoders
Name:           mlt
Version:        0.6.2
Release:        1%{?dist}

License:        GPLv2+ and LGPLv2+
URL:            http://www.mltframework.org/twiki/bin/view/MLT/
Group:          System Environment/Libraries
Source:         http://downloads.sourceforge.net/project/mlt/mlt/mlt-%{version}.tar.gz
Source1:	mlt++-config.h
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


BuildRequires:  frei0r-devel
BuildRequires:  ffmpeg-devel
BuildRequires:  qt-devel
BuildRequires:  libquicktime-devel
BuildRequires:  SDL-devel
BuildRequires:  gtk2-devel
BuildRequires:  jack-audio-connection-kit-devel
BuildRequires:  libogg-devel
BuildRequires:  libdv-devel
BuildRequires:  libvorbis-devel
BuildRequires:  libsamplerate-devel
BuildRequires:  ladspa-devel
BuildRequires:  libxml2-devel
BuildRequires:  sox-devel
BuildRequires:  swig
BuildRequires:  python-devel
BuildRequires:  php-devel
BuildRequires:  ruby-devel ruby

%description
MLT is an open source multimedia framework, designed and developed for 
television broadcasting.

It provides a toolkit for broadcasters, video editors,media players, 
transcoders, web streamers and many more types of applications. The 
functionality of the system is provided via an assortment of ready to use 
tools, xml authoring components, and an extendible plug-in based API.


%package devel
Summary:        Libraries, includes to develop applications with %{name}
License:        LGPLv2+
Group:          Development/Libraries
Requires:       pkgconfig
Requires:       %{name} = %{version}-%{release}

%package python
Requires: python
Requires: %{name} = %{version}-%{release}
Summary: Python package to work with MLT

%package ruby
Requires: ruby(abi) = 1.8
Requires: %{name} = %{version}-%{release}
Summary: Ruby package to work with MLT

%package php
Requires: php
Requires: %{name} = %{version}-%{release}
Summary: PHP package to work with MLT

%description devel
The %{name}-devel package contains the header files and static libraries for
building applications which use %{name}.

%description python
This module allows to work with MLT using python. 

%description ruby
This module allows to work with MLT using ruby.

%description php
This module allows to work with MLT using PHP. 


%prep
%setup -q
#%patch1 -p1
install -m 0644 %{SOURCE1} src/mlt++/config.h
find ./ -name configure -exec chmod 755 {} \;
chmod 755 src/modules/lumas/create_lumas
chmod 644 src/modules/qimage/kdenlivetitle_wrapper.cpp
chmod 644 src/modules/kdenlive/filter_freeze.c
chmod -x demo/demo

# Don't optimize (breaks debugging)
sed -i -e '/fomit-frame-pointer/d' configure
sed -i -e '/ffast-math/d' configure


%build
#export STRIP=/bin/true
%configure \
        --enable-gpl                            \
        --enable-motion-est                     \
%ifarch ppc ppc64 
        --disable-mmx                           \
        --disable-sse                           \
        --disable-xine                          \
%endif
        --qimage-libdir=%{_qt4_libdir}          \
        --qimage-includedir=%{_qt4_headerdir}   \
        --rename-melt=%{name}-melt              \
        --avformat-swscale                      \
        --swig-languages='python php ruby'

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
install -d $RPM_BUILD_ROOT%{python_sitelib}
install -d $RPM_BUILD_ROOT%{python_sitearch}
install -d $RPM_BUILD_ROOT%{ruby_sitelib}
install -d $RPM_BUILD_ROOT%{ruby_sitearch}
install -d $RPM_BUILD_ROOT%{php_extdir}
install -pm 0644 src/swig/python/%{name}.py $RPM_BUILD_ROOT%{python_sitelib}/
install -pm 0755 src/swig/ruby/play.rb $RPM_BUILD_ROOT%{ruby_sitelib}/
install -pm 0755 src/swig/ruby/thumbs.rb $RPM_BUILD_ROOT%{ruby_sitelib}/
install -pm 0755 src/swig/ruby/%{name}.so $RPM_BUILD_ROOT%{ruby_sitearch}/
install -pm 0755 src/swig/python/_%{name}.so $RPM_BUILD_ROOT%{python_sitearch}/
install -pm 0755 src/swig/php/%{name}.so $RPM_BUILD_ROOT%{php_extdir}/

mv src/modules/motion_est/README README.motion_est

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING GPL NEWS README*
%{_bindir}/%{name}-melt
%{_libdir}/%{name}
%{_libdir}/*.so.*
%{_datadir}/%{name}


%files python
%defattr(-,root,root,-)
%{python_sitelib}/%{name}.py
%{python_sitelib}/%{name}.pyc
%{python_sitelib}/%{name}.pyo
%{python_sitearch}/_%{name}.so

%files ruby
%defattr(-,root,root,-)
%{ruby_sitelib}/play.rb
%{ruby_sitelib}/thumbs.rb
%{ruby_sitearch}/%{name}.so

%files php
%defattr(-,root,root,-)
%{php_extdir}/%{name}.so

%files devel
%defattr(-,root,root,-)
%doc docs/* demo
%{_libdir}/pkgconfig/*
%{_libdir}/*.so
%{_includedir}/*


%changelog
* Sun Mar 20 2011 Arkady L. Shane <ashejn@yandx-team.ru> - 0.6.2-1
- update to 0.6.2
- drop mmx patch

* Thu Nov  8 2010 Arkady L. Shane <ashejn@yandx-team.ru> - 0.5.10-1
- update to 0.5.10

* Wed Apr 21 2010 Ryan Rix <ry@n.rix.si> - 0.5.4-1
- New upstream version to fix reported crashes against Kdenlive

* Fri Feb 19 2010 Zarko Pintar <zarko.pintar@gmail.com> - 0.5.0-2
- disabled xine module for PPC arch.

* Thu Feb 18 2010 Zarko Pintar <zarko.pintar@gmail.com> - 0.5.0-1
- new version

* Wed Dec 09 2009 Zarko Pintar <zarko.pintar@gmail.com> - 0.4.10-1
- new version
- added subpackage for ruby

* Wed Oct 07 2009 Zarko Pintar <zarko.pintar@gmail.com> - 0.4.6-1
- new version
- added subpackages for: python, PHP

* Mon Sep 07 2009 Zarko Pintar <zarko.pintar@gmail.com> - 0.4.4-1
- new version
- renamed melt binary to mlt-melt

* Wed May 20 2009 Zarko Pintar <zarko.pintar@gmail.com> - 0.4.2-1
- new version
- removed obsolete patches

* Wed May 20 2009 Zarko Pintar <zarko.pintar@gmail.com> - 0.4.0-3
- added linker and license patches
- set license of MLT devel subpackage to LGPLv2+ 

* Wed May 20 2009 Zarko Pintar <zarko.pintar@gmail.com> - 0.4.0-2
- some PPC clearing

* Mon May 18 2009 Zarko Pintar <zarko.pintar@gmail.com> - 0.4.0-1
- update to 0.4.0

* Wed May 13 2009 Zarko Pintar <zarko.pintar@gmail.com> - 0.3.9-2
- spec cleaning

* Mon May 11 2009 Zarko Pintar <zarko.pintar@gmail.com> - 0.3.9-1
- new release
- MLT++  is now a part of this package

* Fri May  7 2009 Zarko Pintar <zarko.pintar@gmail.com> - 0.3.8-3
- unused-direct-shlib-dependency fix

* Fri Apr 17 2009 Zarko Pintar <zarko.pintar@gmail.com> - 0.3.8-2
- spec clearing
- added patches for resolving broken lqt-config, lib64 and execstack

* Wed Apr 15 2009 Zarko Pintar <zarko.pintar@gmail.com> - 0.3.8-1
- New release

* Thu Apr  9 2009 Zarko Pintar <zarko.pintar@gmail.com> - 0.3.6-3
- Enabled MMX support (not for PPC & PPC64)
- include demo files
- some spec cosmetics

* Thu Mar 12 2009 Zarko Pintar <zarko.pintar@gmail.com> - 0.3.6-2
- Change URL address
- devel Requires: pkgconfig

* Fri Feb 20 2009 Levente Farkas <lfarkas@lfarkas.org> - 0.3.6-1
- Update to 0.3.6

* Wed Nov  5 2008 Arkady L. Shane <ashejn@yandex-team.ru> - 0.3.1-0.1.svn1180
- update to upstream r1180
- add --avformat-swscale configure option

* Tue Nov  4 2008 Arkady L. Shane <ashejn@yandex-team.ru> - 0.3.0-5
- rebuilt with proper qt4 paths

* Mon Oct 13 2008 jeff <moe@blagblagblag.org> - 0.3.0-4
- Build without fomit-frame-pointer ffmath
- Add BuildRequires: prelink
- clear-execstack libmltgtk2.so
- Don't strip binaries
- Group: Development/Libraries
- Prefix albino, humperdink, and miracle binaries with mlt-

* Sun Oct  5 2008 jeff <moe@blagblagblag.org> - 0.3.0-3
- License: GPLv2+ and LGPLv2+
- Group: Development/Tools
- ExcludeArch: x86_64 s390 s390x ppc ppc64
- %%defattr(-,root,root)
- %%doc docs/
- %%{_libdir}/%%{name} to main package


* Sun Aug 24 2008 jeff <moe@blagblagblag.org> - 0.3.0-2
- Change BuildRoot:
- Full source URL
- ExcludeArch: x86_64
- -devel Requires: pkgconfig, Requires: %%{name} = %%{version}-%%{release}

* Sun Aug 24 2008 jeff <moe@blagblagblag.org> - 0.3.0-1
- Update to 0.3.0
- --enable-gpl
- mlt-filehandler.patch

* Tue Jul  8 2008 jeff <moe@blagblagblag.org> - 0.2.5-0.svn1155.0blag.f10
- Build for blaghead

* Mon Jul  7 2008 jeff <moe@blagblagblag.org> - 0.2.5-0.svn1155.0blag.f9
- Update to svn r1155
- Remove sox-st.h.patch
- Add configure --disable-sox as it breaks build

* Sun Nov 11 2007 jeff <moe@blagblagblag.org> - 0.2.4-0blag.f7
- Update to 0.2.4
- Clean up spec

* Sat Jun 23 2007 jeff <moe@blagblagblag.org> - 0.2.3-0blag.f7
- Update to 0.2.3

* Sat Dec 30 2006 jeff <moe@blagblagblag.org> - 0.2.2-0blag.fc6
- Rebuild for 60k
- Remove --disable-sox
- Add mlt-0.2.2-sox-st.h.patch

* Sat Oct 21 2006 jeff <moe@blagblagblag.org> - 0.2.2-0blag.fc5
- Update to 0.2.2

* Sat Oct 21 2006 jeff <moe@blagblagblag.org> - 0.2.1-0blag.fc5
- BLAG'd
- Removed "olib" from path, name, etc.
- Add changelog
- Update summary/description

