import io
import mmap
import os

MAX_SIZE = 10000

class FileSharing():
    def __init__(self, filename):
        self.len = os.stat(filename).st_size
        self.filename = filename

        # grow the file
        file = open(filename, "ab")
        file.write(bytes("\0" * (MAX_SIZE - self.len), encoding='utf8'))
        file.flush()
        file.close()

        # now open the new file
        self.file =  open(filename, "r+b")
        self.mm = mmap.mmap(self.file.fileno(), MAX_SIZE)

    def close(self):
        self.mm.flush()
        data = self.mm[:self.len]
        self.mm.close()
        self.file.truncate(self.len)
        self.file.close()
        
    def put(self, offset, string):
        strlen = len(string)
        self.mm.move(offset + strlen, offset, self.len - offset)
        self.mm.seek(offset)
        self.mm.write(bytes(string, encoding='utf8'))
        self.mm.flush()
        self.len += strlen
        
    def delete(self, offset, length):
        self.mm.move(offset, offset + length, self.len - offset - length)
        self.mm.flush()
        self.len -= length

    def get(self):
        return ''.join(chr(i) for i in (self.mm[:self.len]))

if __name__ == '__main__':
    fs = FileSharing('hello.txt')
    fs.put(fs.len, 'abc')
    print(fs.get())
    fs.close()
