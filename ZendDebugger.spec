# NOTE
# - Can't find what Free Download means (http://www.zend.com/free_download/list)
# - dummy.php should be placed to document root

# Unusable in PLD Linux as our PHP is compiled with ZTS, while this extension is not
%define		_zend_zts	0

Summary:	The Zend Debug Server enabling remote debugging of PHP applications
Summary(pl.UTF-8):	Zend Debug Server pozwalający na zdalne śledzenie aplikacji PHP
Name:		ZendDebugger
Version:	20100729
Release:	0.1
License:	Free Download
Group:		Development/Languages/PHP
Source0:	http://downloads.zend.com/studio_debugger/20100729/%{name}-%{version}-linux-glibc23-i386.tar.gz
# NoSource0-md5:	6112762c697af055d65e77f4b5705c17
NoSource:	0
Source1:	http://downloads.zend.com/studio_debugger/20100729/%{name}-%{version}-linux-glibc23-x86_64.tar.gz
# NoSource1-md5:	5423c72de2e4715663186ea5c6cc0ab0
NoSource:	1
URL:		http://www.zend.com/store/software/zend_studio
BuildRequires:	php-devel
BuildRequires:	rpmbuild(macros) >= 1.553
BuildRequires:	tar >= 1:1.15.1
Obsoletes:	php-ZendDebugger
Obsoletes:	php4-ZendDebugger
Conflicts:	ZendStudioServer <= 5.2.0
%{?requires_php_extension}
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# No debuginfo to be stored
%define		_enable_debug_packages	0

%description
The Zend Debug Server enables remote debugging of PHP applications. It
plugs into a PHP server and allows the Zend Development Environment to
control the execution of PHP applications on the server.

The Debug Server is designed be deployed safely on production servers.
It does not affect server performance and features access-list based
security for protecting the server from unauthorized access.

%description -l pl.UTF-8
Zend Debug Server pozwala na zdalne śledzenie aplikacji PHP. Podłącza
się do serwera PHP i pozwala środowisku Zend Development Environment
sterować wykonywaniem aplikacji PHP na serwerze.

Debug server jest zaprojektowany z myślą o bezpiecznym wdrożeniu na
serwerach produkcyjnych. Nie wpływa na wydajność serwera i cechuje się
bezpieczeństwem opartym na listach dostępu.

%prep
%setup -qcT
%ifarch %{x8664}
%{__tar} --strip-components=1 -xzf %{SOURCE1}
%else
%{__tar} --strip-components=1 -xzf %{SOURCE0}
%endif

%undos dummy.php README

cat > zend.ini <<EOF
[Zend]
zend_debugger.allow_hosts=127.0.0.1
zend_debugger.expose_remotely=always
EOF

cat <<'EOF' > pack.ini
; %{name} package settings. Overwritten with each upgrade.
; if you need to add options, edit %{name}.ini instead
[Zend]
zend_extension=%{php_extensiondir}/ZendDebugger.so
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}
install -p %{php_major_version}_%{php_minor_version}_x_comp/ZendDebugger.so $RPM_BUILD_ROOT%{php_extensiondir}
cp -a zend.ini $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{name}.ini
cp -a pack.ini $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{name}_pack.ini

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = "0" ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc README dummy.php
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{name}.ini
%config %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{name}_pack.ini
%attr(755,root,root) %{php_extensiondir}/ZendDebugger.so
