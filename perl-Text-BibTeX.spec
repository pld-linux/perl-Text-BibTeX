#
# Conditional build:
%bcond_without	tests	# unit tests
#
%define		pdir	Text
%define		pnam	BibTeX
Summary:	Text::BibTeX - Perl library for reading, parsing and processing BibTeX files
Summary(pl.UTF-8):	Text::BibTeX - biblioteka Perla do odczytu, analizy i przetwarzania plików BibTeXa
Name:		perl-Text-BibTeX
Version:	0.88
Release:	4
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/Text/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	361aad5cf400764e35d1ade3b609bb60
Patch0:		%{name}-mansect.patch
Patch1:		%{name}-libdir.patch
URL:		http://www.gerg.ca/software/btOOL/
BuildRequires:	perl-Capture-Tiny >= 0.06
BuildRequires:	perl-Config-AutoConf >= 0.16
BuildRequires:	perl-ExtUtils-CBuilder >= 0.27
BuildRequires:	perl-ExtUtils-LibBuilder >= 0.02
BuildRequires:	perl-Module-Build >= 0.3603
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{with tests}
BuildRequires:	perl-Scalar-List-Utils >= 1.42
BuildRequires:	perl-Unicode-Normalize
%endif
Requires:	btparse = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Text::BibTeX is a Perl library for reading, parsing, and processing
BibTeX files. It is the Perl half of btOOL, a pair of libraries for
dealing with BibTeX data.

%description -l pl.UTF-8
Text::BibTeX to biblioteka Perla do odczytu, analizy i przetwarzania
plików BibTeXa. Jest to perlowa połowa projektu btOOL - pary bibliotek
do obsługi danych BibTeXa.

%package -n btparse
Summary:	C library to parse BibTeX files
Summary(pl.UTF-8):	Biblioteka C do analizy plików BibTeXa
Group:		Libraries

%description -n btparse
btparse is the C component of btOOL, a pair of libraries for parsing
and processing BibTeX files. Its primary use is as the back-end to
Text::BibTeX library for Perl (the other half of btOOL), but there's
nothing to prevent you from writing C programs using btparse - or from
writing extensions to other high-level languages using btparse as a
back-end.

%description -n btparse -l pl.UTF-8
btparse to część C narzędzia btOOL - pary bibliotek do analizy i
przetwarzania plików BibTeX. Głównym zastosowaniem jest backend dla
biblioteki Text::BibTeX dla Perla (drugiej połówki narzędzia btOOL),
ale nic nie stoi na przeszkodzie pisaniu programów w C
wykorzystujących btparse albo rozszerzeń dla innych wysokopoziomowych
języków z wykorzystaniem btparse jako backendu.

%package -n btparse-devel
Summary:	Header files for btparse library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki btparse
Group:		Development/Libraries
Requires:	btparse = %{version}-%{release}
Obsoletes:	btparse-static < %{version}

%description -n btparse-devel
Header files for btparse library.

%description -n btparse-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki btparse.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}
%patch0 -p1
%patch1 -p1

%build
LIBDIR=%{_libdir} \
%{__perl} Build.PL \
	--config cc="%{__cc}" \
	--config optimize="%{rpmcflags}" \
	installdirs=vendor
./Build

%{?with_tests:./Build test}

%install
rm -rf $RPM_BUILD_ROOT

./Build install \
	destdir=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{perl_vendorarch}/auto/Text/BibTeX/BibTeX.bs

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n btparse -p /sbin/ldconfig
%postun	-n btparse -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc Changes README
%{perl_vendorarch}/Text/BibTeX.pm
%{perl_vendorarch}/Text/BibTeX
%dir %{perl_vendorarch}/auto/Text/BibTeX
%attr(755,root,root) %{perl_vendorarch}/auto/Text/BibTeX/BibTeX.so
%{_mandir}/man3/Text::BibTeX.3pm*
%{_mandir}/man3/Text::BibTeX::*.3pm*

%files -n btparse
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/biblex
%attr(755,root,root) %{_bindir}/bibparse
%attr(755,root,root) %{_bindir}/dumpnames
%attr(755,root,root) %{_libdir}/libbtparse.so

%files -n btparse-devel
%defattr(644,root,root,755)
%{_includedir}/btparse.h
%{_mandir}/man3/bt_*.3*
%{_mandir}/man3/btparse.3*
%{_mandir}/man3/btool_faq.3*
