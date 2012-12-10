#Module-Specific definitions
%define apache_version 2.4.0
%define mod_name mod_authz_unixgroup
%define mod_conf A57_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Apache Unix Group Access Control Modules
Name:		apache-%{mod_name}
Version:	1.1.0
Release:	1
Group:		System/Servers
License:	Apache License
URL:		http://code.google.com/p/mod-auth-external/wiki/ModAuthzUnixGroup
Source0:	http://mod-auth-external.googlecode.com/files/%{mod_name}-%{version}.tar.gz
Source1:	%{mod_conf}
Requires:	pwauth
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):  apache-conf >= %{apache_version}
Requires(pre):  apache >= %{apache_version}
Requires:	apache-conf >= %{apache_version}
Requires:	apache >= %{apache_version}
BuildRequires:  apache-devel >= %{apache_version}

%description
Mod_Authz_Unixgroup is a unix group access control modules for Apache 2.1 and
later. If you are having users authenticate with real Unix login ID over the
net, using something like my mod_authnz_external / pwauth combination, and you
want to do access control based on unix group membership, then
mod_authz_unixgroup is exactly what you need.

%prep

%setup -q -n %{mod_name}-%{version}

chmod 644 CHANGES INSTALL README

rm -rf .libs

cp %{SOURCE1} %{mod_conf}


%build

%{_bindir}/apxs -c %{mod_name}.c

%install

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
        %{_initrddir}/httpd restart 1>&2
    fi
fi

%files
%doc CHANGES INSTALL README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}




%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-6mdv2012.0
+ Revision: 772594
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-5
+ Revision: 678280
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-4mdv2011.0
+ Revision: 587938
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-3mdv2010.1
+ Revision: 516066
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-2mdv2010.0
+ Revision: 406550
- rebuild

* Sun Jun 21 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-1mdv2010.0
+ Revision: 387623
- 1.0.2
- new url
- fix the config

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-2mdv2009.1
+ Revision: 325616
- rebuild

* Sun Aug 10 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-1mdv2009.0
+ Revision: 270226
- 1.0.1

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-7mdv2009.0
+ Revision: 234751
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-6mdv2009.0
+ Revision: 215546
- fix rebuild
- fix buildroot

* Fri Mar 07 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-5mdv2008.1
+ Revision: 181697
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-4mdv2008.0
+ Revision: 82533
- rebuild


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-3mdv2007.1
+ Revision: 140645
- rebuild

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-2mdv2007.1
+ Revision: 79351
- Import apache-mod_authz_unixgroup

* Mon Aug 07 2006 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-2mdv2007.0
- rebuild

* Wed Mar 29 2006 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-1mdk
- initial Mandriva package

