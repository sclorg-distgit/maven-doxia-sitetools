%{?scl:%scl_package %{parent}-%{subproj}}
%{!?scl:%global pkg_name %{name}}

%bcond_without  markdown
%bcond_without  fop

%global parent maven-doxia
%global subproj sitetools

Name:           %{?scl_prefix}%{parent}-%{subproj}
Version:        1.7.4
Release:        3.2%{?dist}
Summary:        Doxia content generation framework
License:        ASL 2.0
URL:            http://maven.apache.org/doxia/
BuildArch:      noarch

Source0:        http://repo2.maven.org/maven2/org/apache/maven/doxia/doxia-sitetools/%{version}/doxia-%{subproj}-%{version}-source-release.zip

Patch0:         0001-Port-to-plexus-utils-3.0.24.patch
Patch1:         0002-Remove-dependency-on-velocity-tools.patch

BuildRequires:  %{?scl_prefix}maven-local
BuildRequires:  %{?scl_prefix}mvn(commons-collections:commons-collections)
BuildRequires:  %{?scl_prefix}mvn(commons-io:commons-io)
BuildRequires:  %{?scl_prefix}mvn(commons-lang:commons-lang)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.doxia:doxia-core)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.doxia:doxia-logging-api)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.doxia:doxia-module-apt)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.doxia:doxia-module-fml)
%if %{with fop}
BuildRequires:  mvn(org.apache.maven.doxia:doxia-module-fo)
%endif
%if %{with markdown}
BuildRequires:  mvn(org.apache.maven.doxia:doxia-module-markdown)
%endif
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.doxia:doxia-module-xdoc)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.doxia:doxia-module-xhtml)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.doxia:doxia-sink-api)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven:maven-artifact)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven:maven-artifact:2.2.1)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven:maven-artifact-manager)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven:maven-model:2.2.1)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven:maven-parent:pom:)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven:maven-project)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.reporting:maven-reporting-api)
BuildRequires:  %{?scl_prefix}mvn(org.apache.velocity:velocity)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.modello:modello-maven-plugin)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.plexus:plexus-component-annotations)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.plexus:plexus-component-metadata)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.plexus:plexus-container-default)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.plexus:plexus-i18n)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.plexus:plexus-interpolation)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.plexus:plexus-velocity)
BuildRequires:  %{?scl_prefix}mvn(xalan:xalan)
BuildRequires:  %{?scl_prefix}mvn(xml-apis:xml-apis)

Provides:      %{?scl_prefix}maven-doxia-tools = %{version}-%{release}

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
%patch0 -p1
%patch1 -p1

# complains
%pom_remove_plugin :apache-rat-plugin
%pom_remove_plugin :maven-enforcer-plugin

%pom_remove_plugin org.codehaus.mojo:clirr-maven-plugin
%pom_remove_dep net.sourceforge.htmlunit:htmlunit doxia-site-renderer/pom.xml
%pom_remove_dep -r :velocity-tools

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
%pom_remove_dep -r :doxia-module-itext

%if %{without markdown}
%pom_remove_dep -r :doxia-module-markdown
%endif
%if %{without fop}
%pom_remove_dep -r :doxia-module-fo
rm -r doxia-doc-renderer/src/main/java/org/apache/maven/doxia/docrenderer/pdf/fo
%endif

%mvn_alias :doxia-integration-tools org.apache.maven.shared:maven-doxia-tools

%build
# tests can't run because of missing deps
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%dir %{_javadir}/%{pkg_name}

%files javadoc -f .mfiles-javadoc

%changelog
* Thu Jun 22 2017 Michael Simacek <msimacek@redhat.com> - 1.7.4-3.2
- Mass rebuild 2017-06-22

* Wed Jun 21 2017 Java Maintainers <java-maint@redhat.com> - 1.7.4-3.1
- Automated package import and SCL-ization

* Tue Feb 07 2017 Michael Simacek <msimacek@redhat.com> - 1.7.4-3
- Add conditionals for fop and markdown

* Mon Feb 06 2017 Michael Simacek <msimacek@redhat.com> - 1.7.4-2
- Remove dependency on velocity-tools

* Mon Nov 14 2016 Michael Simacek <msimacek@redhat.com> - 1.7.4-1
- Update to upstream version 1.7.4

* Wed Nov 09 2016 Michael Simacek <msimacek@redhat.com> - 1.7.3-1
- Update to upstream version 1.7.3

* Wed Nov 02 2016 Michael Simacek <msimacek@redhat.com> - 1.7.2-1
- Update to upstream version 1.7.2

* Thu May 12 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.7.1-3
- Port to plexus-utils 3.0.24

* Thu May 05 2016 Michael Simacek <msimacek@redhat.com> - 1.7.1-2
- Add Provides and Obsoletes for maven-doxia-tools

* Wed May 04 2016 Michael Simacek <msimacek@redhat.com> - 1.7.1-1
- Update to upstream version 1.7.1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jul 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6-1
- Update to upstream version 1.6

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.4-5
- Use Requires: java-headless rebuild (#1067528)

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-4
- Fix unowned directory

* Tue Oct  1 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-3
- Add missing build dependencies

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

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
