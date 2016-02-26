%global pkg_name maven-doxia-sitetools
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%global parent maven-doxia
%global subproj sitetools

Name:           %{?scl_prefix}%{pkg_name}
Version:        1.4
Release:        3.13%{?dist}
Summary:        Doxia content generation framework
License:        ASL 2.0
URL:            http://maven.apache.org/doxia/

Source0:        http://repo2.maven.org/maven2/org/apache/maven/doxia/doxia-sitetools/%{version}/doxia-%{subproj}-%{version}-source-release.zip

Patch1:         0001-Remove-dependency-on-velocity-tools.patch

BuildRequires:  %{?scl_prefix}maven-local
BuildRequires:  %{?scl_prefix_java_common}mvn(commons-collections:commons-collections)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.doxia:doxia-core)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.doxia:doxia-logging-api)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.doxia:doxia-module-apt)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.doxia:doxia-module-fml)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.doxia:doxia-module-fo)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.doxia:doxia-module-xdoc)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.doxia:doxia-module-xhtml)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.doxia:doxia-sink-api)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven:maven-parent:pom:)
BuildRequires:  %{?scl_prefix}mvn(org.apache.velocity:velocity)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.plexus:plexus-container-default)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.plexus:plexus-i18n)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.plexus:plexus-velocity)
BuildRequires:  %{?scl_prefix_java_common}mvn(xalan:xalan)
BuildRequires:  %{?scl_prefix_java_common}mvn(xml-apis:xml-apis)

BuildArch:      noarch

%description
Doxia is a content generation framework which aims to provide its
users with powerful techniques for generating static and dynamic
content. Doxia can be used to generate static sites in addition to
being incorporated into dynamic content generation systems like blogs,
wikis and content management systems.

%package javadoc
Summary:        Javadoc for %{pkg_name}

%description javadoc
API documentation for %{pkg_name}.

%prep
%setup -q -n doxia-%{subproj}-%{version}
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x

# upstream added support for velocity toolmanager, but it also means new
# dependency on velocity-tools. we don't want to depend on this package
# (it depends on struts 1) so this patch reverts upstream changes
%patch1 -p1
%pom_remove_dep :velocity-tools doxia-site-renderer

%pom_remove_plugin org.codehaus.mojo:clirr-maven-plugin
%pom_remove_dep net.sourceforge.htmlunit:htmlunit doxia-site-renderer/pom.xml

%pom_xpath_inject "pom:plugin[pom:artifactId[text()='modello-maven-plugin']]/pom:configuration" \
    "<useJava5>true</useJava5>" doxia-decoration-model

# There are two backends for generating PDFs: one based on iText and
# one using FOP.  iText module is broken and only brings additional
# dependencies.  Besides that upstream admits that iText support will
# likely removed in future versions of Doxia.  In Fedora we remove
# iText backend sooner in order to fix dependency problems.
#
# See also: http://maven.apache.org/doxia/faq.html#How_to_export_in_PDF
# http://lists.fedoraproject.org/pipermail/java-devel/2013-April/004742.html
rm -rf $(find -type d -name itext)
%pom_remove_dep :itext doxia-doc-renderer
%pom_remove_dep :doxia-module-itext doxia-doc-renderer
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
# tests can't run because of missing deps
%mvn_build -f
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%mvn_install
%{?scl:EOF}


%files -f .mfiles
%{_javadir}/%{pkg_name}
%dir %{_mavenpomdir}/%{pkg_name}

%files javadoc -f .mfiles-javadoc

%changelog
* Mon Feb 08 2016 Michal Srb <msrb@redhat.com> - 1.4-3.13
- Fix BR on maven-local & co.

* Mon Jan 11 2016 Michal Srb <msrb@redhat.com> - 1.4-3.12
- maven33 rebuild #2

* Sat Jan 09 2016 Michal Srb <msrb@redhat.com> - 1.4-3.11
- maven33 rebuild

* Thu Jan 15 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-3.10
- Add directory ownership on %%{_mavenpomdir} subdir

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 1.4-3.9
- Mass rebuild 2015-01-13

* Mon Jan 12 2015 Michael Simacek <msimacek@redhat.com> - 1.4-3.8
- Rebuild to regenerate requires from java-common

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 1.4-3.7
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-3.6
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-3.5
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-3.4
- Mass rebuild 2014-02-18

* Mon Feb 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-3.3
- SCL-ize build-requires

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-3.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-3.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.4-3
- Mass rebuild 2013-12-27

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-2
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Mon Apr 29 2013 Michal Srb <msrb@redhat.com> - 1.4-1
- Update to upstream version 1.4
- Remove unneeded patch

* Tue Apr  9 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3-4
- Fix BuildRequires

* Tue Apr  9 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3-3
- Remove iText PDF backend

* Tue Apr 09 2013 Michal Srb <msrb@redhat.com>
- Remove dependency on velocity-tools

* Wed Feb 06 2013 Michal Srb <msrb@redhat.com> - 1.3-1
- Update to upstream version 1.3
- Migrate from maven-doxia to doxia subpackages (#889145)
- Build with xmvn
- Replace patches with pom_ macros
- Remove unnecessary depmap

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.2-6
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Wed Nov 28 2012 Tomas Radej <tradej@redhat.com> - 1.2-5
- Removed (B)R on plexus-container-default

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 27 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.2-3
- Remove dependency on plexux-xmlrpc
- Add BR/R on java 1.7.0+

* Mon Jan 09 2012 Jaromir Capik <jcapik@redhat.com> - 1.2-2
- Migration from plexus-maven-plugin to plexus-containers-component-metadata
- Minor spec file changes according to the latest guidelines

* Fri May  6 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.2-1
- Update to latest version (1.2)
- Use maven 3 to build
- Remove version limits on BR/R (not valid anymore anyway)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Alexander Kurtakov <akurtako@redhat.com> 1.1.3-2
- Adapt to current guidelines.

* Tue Sep  7 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.1.3-1
- Update to 1.1.3
- Enable javadoc generation again
- Update maven plugins BRs
- Make dependency on maven-doxia unversioned

* Thu Jun 17 2010 Deepak Bhole <dbhole@redhat.com> - 0:1.1.2-3
- Rebuild with maven 2.2.1
- Remove modello 1.0 patch

* Wed May  5 2010 Mary Ellen Foster <mefoster at gmail.com> 0:1.1.2-2
- Add (Build)Requirement maven-shared-reporting-impl,
  plexus-containers-container-default, jakarta-commons-configuration

* Fri Feb 12 2010 Mary Ellen Foster <mefoster at gmail.com> 0:1.1.2-1
- Update to 1.1.2
- Temporarily disable javadoc until maven2-plugin-javadoc is rebuilt against
  the new doxia

* Mon Dec 21 2009 Alexander Kurtakov <akurtako@redhat.com> 1.0-0.2.a10.2
- BR maven-surefire-provider-junit.

* Tue Sep 01 2009 Andrew Overholt <overholt@redhat.com> 1.0-0.2.a10.1
- Add itext, tomcat5, and tomcat5-servlet-2.4-api BRs

* Fri Aug 28 2009 Andrew Overholt <overholt@redhat.com> 1.0-0.2.a10
- First Fedora build

* Fri Jun 20 2000 Deepak Bhole <dbhole@redhat.com> 1.0-0.1.a10.0jpp.1
- Initial build
