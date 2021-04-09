# raspiGO

RaspiGo to system umożliwiający utworzenie domowego netflixa z twojej prywatnej biblioteki filmów i seriali. System jest dedykowany dla komputera Raspberry Pi pod kontrolą systemu operacyjnego Raspberry Pi OS.

Backend oprogramowania utworzony został we Flasku oraz SQLAlchemy. Frontend korzysta z Bootstrapa w wersji 4.

# Funkcjonalność

## Automatyczne pobieranie informacji o filmie/serialu

Po dodaniu nowych treści do systemu wszystkie potrzebne informację zostaną pobrane automatycznie. Jedyne działanie użytkownika to umieszczenie pliku z video w katalogu o nazwie będącej tytułem filmu/serialu.

System automatycznie pobierze:

- podstawowe informację o filmie/serialu wraz z oceną z filmwebu

- ocenę filmu/serialu z IMDB

- grafikę z filmu/serialu

  

Gdyby któreś z informacji zostały źle wyszukane to system umożliwia edytowanie wszystkich informacji z poziomu panelu ustawień. W szczególności w sytuacji doboru złych linków system umożliwia podanie nowych i ponowne automatyczne pobranie z nich treści.

## Konta użytkowników

System implementuję konta użytkowników w celu personalizacji treści. Użytkownik może śledzić kategorię - zmienia to układ jego strony głównej. Ponadto system implementuję **historię oglądania** indywidualną dla każdego użytkownika.

## Historia oglądania

Ostatnio obejrzane treści zostają dodane do historii oglądania. Sekcja z tymi treściami pojawia się jako pierwsza na stronie głównej aby ułatwić powrót do ostatnio oglądanych treści. Zapamiętany zostaję również czas w którym użytkownik zakończył oglądanie. Po powrocie do oglądania film/serial zostaję wznowiony w dokładnie tym samym momencie w którym został przerwany.

## Napisy

Użytkownik może dodać napisy do filmów/seriali przez umieszczenie ich w odpowiednim folderze. System implementuję obsługę napisów w wielu językach. Aktualnie jedynym obsługiwanym formatem jest *.vtt*.

## Rozbudowany panel konfiguracyjny

Po dodanie treści na dysk i podpięciu go do Raspberry użytkownik nie musi mieć żadnego fizycznego kontaktu z maliną. Umożliwia to rozbudowany panel konfiguracyjny, który oferuję wiele funkcji konfiguracyjnych.

## Responsywność

Korzystanie z serwisu przez urządzenia mobilne jest bardzo wygodne ze względu na responsywną technologię wykorzystaną przy budowie front end'u serwisu.

  
  
  

# Instrukcja użytkowania

## Dodawanie nowych treści

Dodanie nowego filmu czy serialu do systemu polega na utworzeniu nowego folderu we wskazanym wcześniej katalogu aplikacji. Struktura katalogu:

![struktura katalogu multimedialnego](https://i.ibb.co/9W1TXyV/Screenshot-from-2021-04-02-15-39-49.png)

Po dodaniu nowych treści należy zaaktualizować system klikając w odpowiednie łączę w panelu ustawień.

Katalogi należy nazywać tytułem treści, aby system wiedział co ma pobrać.

W katalogu należy umieścić plik video oraz ewentualnie napisy.

Nazwa pliku video jest dowolna, natomiast napisy należy nazywać w formie *{język}.vtt*.

W katalogu nie powinno znajdować się nic więcej.

## Konta użytkowników

Aby korzystać z kont należy je najpierw włączyć z poziomu panelu ustawień.

Od teraz każdą pierwszą próbę dostępu do treści poprzedzi strona wyboru kont.

Konta można zawieszać bądź usuwać z poziomu panelu konfiguracyjnego.

Gdy korzystanie z kont zostanie wyłączone, konta nie zostaną usunięte.

  
  

# Instalacja i pierwsza konfiguracja

## Instalacja

  

Zacznij od pobrania aplikacji z githuba:

	git clone https://github.com/kuna728/raspigo

Przejdź do katalogu aplikacji i pobierz wszystkie niezbędne pakiety Pythona:

	cd raspiGO

	pip3 install -r requirements.txt

Do działania aplikacji potrzebny jest odpowiednio zainstalowany pakiet Selenium. Szczegółowa instrukcja instalacji dostępna jest na stronie *https://qabrio.pl/selenium-w-embedded-instalacja-na-raspberry-pi/*.

Wszystkie potrzebne rzeczy zostały pobrane. Można teraz przejść do pierwszej konfiguracji.

## Konfiguracja systemu operacyjnego

Aby dodać aplikację do autostartu na Raspberry Pi OS otwórz plik */home/pi/.bashrc* w swoim ulubionym edytorze tekstu:

  

sudo nano /home/pi/.bashrc

Następnie dopisz na końcu pliku linijkę:

  

python3 /sciezka_do_katalogu_z_aplikacja/raspigo.py

Aplikacja jest gotowa do uruchomienia:
	
	python3 raspigo.py

  

## Pierwsza konfiguracja aplikacji

Dostęp do aplikacji możesz uzyskać pod adresem *<adres_ip_raspberryPi>:5000*. Aby sprawdzić adres IP maliny możesz skorzystać z komedy *ifconfig* lub z poziomu panelu konfiguracyjnego routera.
Po wgraniu treści do Raspberry bądź podłączeniu dysku zewnętrznego ustal jego lokalizację. Następnie w panelu ustawień podaj ścieżkę do folderu *raspigo* z treścią. Teraz można przystąpić do dodania treści do aplikacji. Kliknij w odnośnik *Wymuś aktualizację* na stronie głównej panelu ustawień. W przypadku dużej ilości treści operacja ta może chwilę potrwać.
System jest gotowy do użytkowania.
