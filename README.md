# RUNSIBLE / RUnsible / RU.NSIBLE 

<p dir="auto" style="text-align: center;"><em>Данный проект написан ПОЛНОСТЬЮ с нуля</em></p>
<p dir="auto" style="text-align: center;">Написал инженер-программист&nbsp;<strong>Ткачук (Коновалов) Денис</strong>&nbsp;-&nbsp;<a href="mailto:where.adm@mail.ru">where.adm@mail.ru</a></p>

<p dir="auto">&nbsp;</p>


<div>
  <p dir="auto"><strong>RUnsible</strong> (или <strong>RUNsible</strong>) -Российский аналог Ansible.</p>
<div>Какие отличия:</div>
<div>1. Нет привязанности к YAML формату. Теперь неважно правильно поставили пробел или Нет.</div>
<div>2. Понятный CallBack без плагинов. Теперь все логи можно увидеть так, как они были. Больше никакой непонятной чихарды</div>
</div>
<li>
<p><strong>Запустите инструмент:</strong></p>
<div class="dark bg-gray-950 contain-inline-size rounded-md border-[0.5px] border-token-border-medium relative">
<div class="flex items-center text-token-text-secondary bg-token-main-surface-secondary px-4 py-2 text-xs font-sans justify-between rounded-t-md h-9">&nbsp;</div>
<div class="sticky top-9 md:top-[5.75rem]">&nbsp;</div>
<div class="overflow-y-auto p-4" dir="ltr"><code class="!whitespace-pre hljs language-csharp">python main.py -group mygroup -bash "hostname" </code></div>
<div class="overflow-y-auto p-4" dir="ltr"><code class="!whitespace-pre hljs language-csharp">python main.py -group mygroup -sh ./script.sh </code></div>
</div>
</li>
<h2><strong>Возможности и параметры командной строки</strong></h2>
<h3><strong>Общие параметры</strong></h3>
<ul>
<li>
<p><code>-group</code><br />Указывает группу хостов для подключения и выполнения команд. Если не указано, по умолчанию используется группа <code>all</code>.</p>
<p><strong>Пример использования:</strong></p>
<div class="dark bg-gray-950 contain-inline-size rounded-md border-[0.5px] border-token-border-medium relative">
<div class="flex items-center text-token-text-secondary bg-token-main-surface-secondary px-4 py-2 text-xs font-sans justify-between rounded-t-md h-9">&nbsp;</div>
<div class="sticky top-9 md:top-[5.75rem]">&nbsp;</div>
<div class="overflow-y-auto p-4" dir="ltr"><code class="!whitespace-pre hljs language-csharp">python main.py -group mygroup </code></div>
</div>
</li>
<li>
<p><code>-i</code><br />Указывает путь к файлу инвентаризации (inventory file), где перечислены хосты и группы. Если не указано, используется файл <code>hosts</code> в той же директории, что и <code>main.py</code>.</p>
<p><strong>Пример использования:</strong></p>
<div class="dark bg-gray-950 contain-inline-size rounded-md border-[0.5px] border-token-border-medium relative">
<div class="flex items-center text-token-text-secondary bg-token-main-surface-secondary px-4 py-2 text-xs font-sans justify-between rounded-t-md h-9">&nbsp;</div>
<div class="sticky top-9 md:top-[5.75rem]">&nbsp;</div>
<div class="overflow-y-auto p-4" dir="ltr"><code class="!whitespace-pre hljs language-css">python main.py -i /path/to/my_hosts </code></div>
</div>
</li>
<li>
<p><code>-key</code><br />Указывает путь к приватному SSH-ключу для аутентификации. Если не указано, используется SSH-ключ по умолчанию <code>~/.ssh/id_rsa</code>.</p>
<p><strong>Пример использования:</strong></p>
<div class="dark bg-gray-950 contain-inline-size rounded-md border-[0.5px] border-token-border-medium relative">
<div class="flex items-center text-token-text-secondary bg-token-main-surface-secondary px-4 py-2 text-xs font-sans justify-between rounded-t-md h-9">&nbsp;</div>
<div class="sticky top-9 md:top-[5.75rem]">&nbsp;</div>
<div class="overflow-y-auto p-4" dir="ltr"><code class="!whitespace-pre hljs language-css">python main.py -key /path/to/private_key </code></div>
</div>
</li>
</ul>
<h3><strong>Выполнение команд и скриптов</strong></h3>
<ul>
<li>
<p><code>-bash</code><br />Позволяет выполнить команду Bash напрямую на удаленных хостах без загрузки скрипта.</p>
<p><strong>Пример использования:</strong></p>
<div class="dark bg-gray-950 contain-inline-size rounded-md border-[0.5px] border-token-border-medium relative">
<div class="flex items-center text-token-text-secondary bg-token-main-surface-secondary px-4 py-2 text-xs font-sans justify-between rounded-t-md h-9">&nbsp;</div>
<div class="sticky top-9 md:top-[5.75rem]">&nbsp;</div>
<div class="overflow-y-auto p-4" dir="ltr"><code class="!whitespace-pre hljs language-csharp">python main.py -group mygroup -bash "echo 'Hello World'"</code></div>
</div>
</li>
<li>
<p><code>-sh</code><br />Указывает путь к локальному bash-скрипту, который будет загружен на удаленные хосты, выполнен и затем удален.</p>
<p><strong>Пример использования:</strong></p>
<div class="dark bg-gray-950 contain-inline-size rounded-md border-[0.5px] border-token-border-medium relative">
<div class="flex items-center text-token-text-secondary bg-token-main-surface-secondary px-4 py-2 text-xs font-sans justify-between rounded-t-md h-9">&nbsp;</div>
<div class="sticky top-9 md:top-[5.75rem]">&nbsp;</div>
<div class="overflow-y-auto p-4" dir="ltr"><code class="!whitespace-pre hljs language-csharp">python main.py -group mygroup -sh script.sh </code></div>
</div>
</li>
<li>
<p><code>-remote_path</code><br />Указывает путь на удаленном хосте, куда будет загружен скрипт, указанный в <code>-sh</code>. По умолчанию используется <code>/tmp</code>.</p>
<p><strong>Пример использования:</strong></p>
<div class="dark bg-gray-950 contain-inline-size rounded-md border-[0.5px] border-token-border-medium relative">
<div class="flex items-center text-token-text-secondary bg-token-main-surface-secondary px-4 py-2 text-xs font-sans justify-between rounded-t-md h-9">&nbsp;</div>
<div class="sticky top-9 md:top-[5.75rem]">&nbsp;</div>
<div class="overflow-y-auto p-4" dir="ltr"><code class="!whitespace-pre hljs language-sql">python main.py -group mygroup -sh script.sh -remote_path /home/user/scripts </code></div>
</div>
</li>
</ul>
<h3><strong>Дополнительные параметры</strong></h3>
<ul>
<li>
<p><code>-help</code><br />Выводит справочную информацию о параметрах и возможностях инструмента.</p>
<p><strong>Пример использования:</strong></p>
<div class="dark bg-gray-950 contain-inline-size rounded-md border-[0.5px] border-token-border-medium relative">
<div class="flex items-center text-token-text-secondary bg-token-main-surface-secondary px-4 py-2 text-xs font-sans justify-between rounded-t-md h-9">&nbsp;</div>
<div class="sticky top-9 md:top-[5.75rem]">&nbsp;</div>
<div class="overflow-y-auto p-4" dir="ltr"><code class="!whitespace-pre hljs language-bash">python main.py -help </code></div>
</div>
</li>
</ul>
<h2><strong>Примеры использования</strong></h2>
<ol>
<li>
<p><strong>Выполнение команды Bash напрямую на группе хостов:</strong></p>
<div class="dark bg-gray-950 contain-inline-size rounded-md border-[0.5px] border-token-border-medium relative">
<div class="flex items-center text-token-text-secondary bg-token-main-surface-secondary px-4 py-2 text-xs font-sans justify-between rounded-t-md h-9">&nbsp;</div>
<div class="sticky top-9 md:top-[5.75rem]">&nbsp;</div>
<div class="overflow-y-auto p-4" dir="ltr"><code class="!whitespace-pre hljs language-csharp">python main.py -group servers -bash "uptime"</code></div>
</div>
<p><em>Выполнит команду <code>uptime</code> на всех хостах, входящих в группу <code>servers</code>.</em></p>
</li>
<li>
<p><strong>Выполнение локального скрипта на удаленных хостах:</strong></p>
<div class="dark bg-gray-950 contain-inline-size rounded-md border-[0.5px] border-token-border-medium relative">
<div class="flex items-center text-token-text-secondary bg-token-main-surface-secondary px-4 py-2 text-xs font-sans justify-between rounded-t-md h-9">&nbsp;</div>
<div class="sticky top-9 md:top-[5.75rem]">&nbsp;</div>
<div class="overflow-y-auto p-4" dir="ltr"><code class="!whitespace-pre hljs language-csharp">python main.py -group webservers -sh deploy.sh </code></div>
</div>
<p><em>Загрузит локальный скрипт <code>deploy.sh</code> на удаленные хосты из группы <code>webservers</code>, выполнит его и удалит после выполнения.</em></p>
</li>
<li>
<p><strong>Указание кастомного файла инвентаризации и SSH-ключа:</strong></p>
<div class="dark bg-gray-950 contain-inline-size rounded-md border-[0.5px] border-token-border-medium relative">
<div class="flex items-center text-token-text-secondary bg-token-main-surface-secondary px-4 py-2 text-xs font-sans justify-between rounded-t-md h-9">&nbsp;</div>
<div class="sticky top-9 md:top-[5.75rem]">&nbsp;</div>
<div class="overflow-y-auto p-4" dir="ltr"><code class="!whitespace-pre hljs language-bash">python main.py -group dbservers -i ./my_hosts -key ~/.ssh/db_key -bash "df -h" </code></div>
</div>
<p><em>Использует файл инвентаризации <code>./my_hosts</code> и SSH-ключ <code>~/.ssh/db_key</code> для подключения к хостам из группы <code>dbservers</code> и выполняет команду <code>df -h</code>.</em></p>
</li>
</ol>
<h2><strong>Формат файла инвентаризации</strong></h2>
<p>Файл инвентаризации (обычно <code>hosts</code>) используется для определения групп хостов и их параметров.</p>
<h3><strong>Пример структуры файла <code>hosts</code>:</strong></h3>
<div class="dark bg-gray-950 contain-inline-size rounded-md border-[0.5px] border-token-border-medium relative">
<div class="flex items-center text-token-text-secondary bg-token-main-surface-secondary px-4 py-2 text-xs font-sans justify-between rounded-t-md h-9">&nbsp;</div>
<div class="sticky top-9 md:top-[5.75rem]">&nbsp;</div>
<div class="overflow-y-auto p-4" dir="ltr"><span class="hljs-selector-attr">[group1]</span></div>
<div class="overflow-y-auto p-4" dir="ltr">host1<span class="hljs-selector-class">.example</span><span class="hljs-selector-class">.com</span> runsible_user=user1 runsible_password=pass1</div>
<div class="overflow-y-auto p-4" dir="ltr"><span class="hljs-number">10.0</span>.<span class="hljs-number">0</span>.{<span class="hljs-number">1</span>:<span class="hljs-number">3</span>} ansible_user=user2 ansible_password=pass2</div>
<div class="overflow-y-auto p-4" dir="ltr"><span class="hljs-number">92.168</span>.<span class="hljs-number">1</span>.{<span class="hljs-number">5</span>..<span class="hljs-number">7</span>}:<span class="hljs-number">2222</span> ansible_user=user3 ansible_password=pass3 [group2]</div>
<div class="overflow-y-auto p-4" dir="ltr">server{<span class="hljs-number">01</span>..<span class="hljs-number">05</span>}<span class="hljs-selector-class">.example</span><span class="hljs-selector-class">.com</span> ansible_user=admin ansible_password=adminpass</div>
</div>
host1.example.com runsible_user=user1 runsible_ssh_key=~/.ssh/host1_key
10.0.0.1 ansible_user=user2 ansible_ssh_private_key_file=/path/to/key2
<h3><strong>Особенности:</strong></h3>
<ul>
<li><strong>Группы хостов</strong> определяются в квадратных скобках <code>[group_name]</code>.</li>
<li><strong>Хосты</strong> могут быть указаны индивидуально или с использованием диапазонов, например, <code>10.0.0.{1:3}</code> или <code>server{01..05}.example.com</code>.</li>
<li><strong>Параметры хоста</strong> могут включать:
<ul>
<li><code>runsible_user</code> или <code>ansible_user</code> &mdash; имя пользователя для подключения по SSH.</li>
<li><code>runsible_password</code> или <code>ansible_password</code> &mdash; пароль для аутентификации.</li>
</ul>
</li>
<li><strong>Указание порта</strong> осуществляется через двоеточие после хоста, например, <code>192.168.1.5:2222</code>.</li>
</ul>
<h2><strong>Замечания</strong></h2>
<ul>
<li>
<p><strong>Порядок приоритетов параметров:</strong></p>
<ul>
<li>Если указаны оба параметра <code>-bash</code> и <code>-sh</code>, будет выполнен скрипт, указанный в <code>-sh</code>.</li>
<li>Если ни <code>-bash</code>, ни <code>-sh</code> не указаны, инструмент не будет знать, что выполнять, и выведет сообщение об ошибке.</li>
</ul>
</li>
<li>
<p><strong>Требования:</strong></p>
<ul>
<li>Python версии 3.x.</li>
<li>Установленный модуль <code>paramiko</code> для работы с SSH.</li>
</ul>
</li>
<li>
<p><strong>Безопасность:</strong></p>
<ul>
<li>При использовании паролей в файле инвентаризации будьте внимательны и соблюдайте меры предосторожности.</li>
<li>Рекомендуется использовать SSH-ключи для аутентификации.</li>
</ul>
</li>
</ul>
<h2><strong>Установка и запуск</strong></h2>
<ol>
<li>
<p><strong>Установите необходимые зависимости:</strong></p>
<div class="dark bg-gray-950 contain-inline-size rounded-md border-[0.5px] border-token-border-medium relative">
<div class="flex items-center text-token-text-secondary bg-token-main-surface-secondary px-4 py-2 text-xs font-sans justify-between rounded-t-md h-9">&nbsp;</div>
<div class="overflow-y-auto p-4" dir="ltr"><code class="!whitespace-pre hljs">pip install paramiko </code></div>
</div>
</li>
<li>
<p><strong>Разместите файлы <code>main.py</code>, <code>inventory.py</code> и <code>playbook.py</code> в одной директории.</strong></p>
</li>
<li>
<p><strong>Создайте файл инвентаризации <code>hosts</code> или используйте свой, указав его с помощью параметра <code>-i</code>.</strong></p>
</li>

</ol>
<h2><strong>Обратная связь</strong></h2>
<p>Если у вас есть вопросы или предложения по улучшению RUNSIBLE, пожалуйста, обращайтесь!</p>
